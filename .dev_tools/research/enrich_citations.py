#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/enrich_citations.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Post-process enrichment for existing citations.

Adds missing supplemental data (citation counts, abstracts, influence metrics)
to citations that only have CrossRef data.

Sources:
1. OpenAlex API (free, comprehensive, citation counts)
2. Semantic Scholar DOI lookup (bypasses query bug)
3. CrossRef is-referenced-by-count (native citation counts)

Usage:
    python enrich_citations.py batch_01_optimization_high.json
    python enrich_citations.py --all  # Enrich all completed batches
"""

import asyncio
import aiohttp
import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EnrichedData:
    """Supplemental data to add to existing citations."""
    citation_count: Optional[int] = None
    abstract: Optional[str] = None
    influence_score: Optional[float] = None
    open_access_url: Optional[str] = None
    source: str = ""


class OpenAlexClient:
    """
    Client for OpenAlex API - free, comprehensive academic database.

    Provides: citation counts, abstracts, open access links, topics
    Rate Limit: 10 requests/second (no auth), 100 req/sec (with email)
    Documentation: https://docs.openalex.org/
    """

    BASE_URL = "https://api.openalex.org"

    def __init__(self, email: Optional[str] = None):
        self.email = email
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        headers = {}
        if self.email:
            headers["User-Agent"] = f"ResearchBot/1.0 (mailto:{self.email})"
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def lookup_by_doi(self, doi: str) -> Optional[EnrichedData]:
        """Lookup paper by DOI and return enriched data."""
        if not doi:
            return None

        url = f"{self.BASE_URL}/works/https://doi.org/{doi}"

        try:
            await asyncio.sleep(0.1)  # 10 req/sec rate limit

            async with self.session.get(url) as resp:
                if resp.status == 404:
                    return None
                resp.raise_for_status()
                data = await resp.json()

                # Extract enriched data
                enriched = EnrichedData(
                    citation_count=data.get('cited_by_count', 0),
                    abstract=self._extract_abstract(data),
                    open_access_url=self._extract_oa_url(data),
                    source='openalex'
                )

                logger.info(f"OpenAlex: Enriched DOI {doi} - {enriched.citation_count} citations")
                return enriched

        except Exception as e:
            logger.warning(f"OpenAlex lookup failed for {doi}: {e}")
            return None

    def _extract_abstract(self, data: Dict) -> Optional[str]:
        """Extract abstract from OpenAlex response."""
        abstract_inv = data.get('abstract_inverted_index')
        if not abstract_inv:
            return None

        # Reconstruct abstract from inverted index
        words = {}
        for word, positions in abstract_inv.items():
            for pos in positions:
                words[pos] = word

        if words:
            return ' '.join(words[i] for i in sorted(words.keys()))
        return None

    def _extract_oa_url(self, data: Dict) -> Optional[str]:
        """Extract open access URL if available."""
        oa_data = data.get('open_access', {})
        return oa_data.get('oa_url')


class SemanticScholarDOIClient:
    """
    Lookup papers by DOI in Semantic Scholar (bypasses query bug).

    Provides: citation counts, abstracts, influence scores
    Rate Limit: 100 requests per 5 minutes
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_request_time = 0

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def lookup_by_doi(self, doi: str) -> Optional[EnrichedData]:
        """Lookup paper by DOI."""
        if not doi:
            return None

        # Rate limiting: 100 req per 5 min = 1 req per 3 seconds
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < 3.0:
            await asyncio.sleep(3.0 - elapsed)

        url = f"{self.BASE_URL}/paper/DOI:{doi}"
        params = {"fields": "citationCount,abstract,influentialCitationCount"}

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        try:
            async with self.session.get(url, params=params, headers=headers) as resp:
                self.last_request_time = time.time()

                if resp.status == 404:
                    return None

                if resp.status == 429:
                    logger.warning("Semantic Scholar rate limit, backing off...")
                    await asyncio.sleep(60)
                    return await self.lookup_by_doi(doi)

                resp.raise_for_status()
                data = await resp.json()

                enriched = EnrichedData(
                    citation_count=data.get('citationCount', 0),
                    abstract=data.get('abstract'),
                    influence_score=data.get('influentialCitationCount', 0),
                    source='semantic_scholar'
                )

                logger.info(f"Semantic Scholar: Enriched DOI {doi} - {enriched.citation_count} citations")
                return enriched

        except Exception as e:
            logger.warning(f"Semantic Scholar lookup failed for {doi}: {e}")
            return None


async def enrich_citation(
    citation: Dict,
    openalex: OpenAlexClient,
    semantic: SemanticScholarDOIClient
) -> Dict:
    """
    Enrich a single citation with supplemental data.

    Strategy:
    1. Try OpenAlex first (faster, more reliable)
    2. Fall back to Semantic Scholar if needed
    3. Keep original data intact
    """
    doi = citation.get('doi')

    # Skip if already has a positive citation count
    if citation.get('citation_count') and citation.get('citation_count') > 0:
        return citation

    # Try OpenAlex first
    enriched = await openalex.lookup_by_doi(doi)

    # Fall back to Semantic Scholar
    if not enriched or enriched.citation_count is None:
        enriched = await semantic.lookup_by_doi(doi)

    # Add enriched data if found
    if enriched:
        if enriched.citation_count is not None:
            citation['citation_count'] = enriched.citation_count
        if enriched.abstract and not citation.get('abstract'):
            citation['abstract'] = enriched.abstract
        if enriched.influence_score is not None:
            citation['influence_score'] = enriched.influence_score
        if enriched.open_access_url:
            citation['open_access_url'] = enriched.open_access_url
        citation['enrichment_source'] = enriched.source

    return citation


async def enrich_batch_file(
    file_path: str,
    email: Optional[str] = None,
    semantic_api_key: Optional[str] = None
) -> Dict[str, int]:
    """Enrich all citations in a batch result file."""

    file_path = Path(file_path)
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return {'error': 1}

    # Load batch data
    with open(file_path) as f:
        data = json.load(f)

    claims = data.get('claims', [])

    stats = {
        'total_citations': 0,
        'enriched': 0,
        'already_complete': 0,
        'failed': 0
    }

    async with OpenAlexClient(email=email) as openalex:
        async with SemanticScholarDOIClient(api_key=semantic_api_key) as semantic:
            for claim in claims:
                if not claim.get('research_completed'):
                    continue

                citations = claim.get('citations', [])
                for citation in citations:
                    stats['total_citations'] += 1

                    # Check if needs enrichment
                    if citation.get('citation_count') and citation.get('citation_count') > 0:
                        stats['already_complete'] += 1
                        continue

                    # Enrich citation
                    try:
                        await enrich_citation(citation, openalex, semantic)
                        # Check if enrichment succeeded by looking for enrichment_source
                        if citation.get('enrichment_source'):
                            stats['enriched'] += 1
                        else:
                            stats['failed'] += 1
                    except Exception as e:
                        logger.error(f"Failed to enrich citation: {e}")
                        stats['failed'] += 1

    # Save enriched data
    output_path = file_path.parent / f"{file_path.stem}_enriched.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved enriched data to {output_path}")
    return stats


async def enrich_research_results(
    file_path: str = "artifacts/research/research_results.json",
    email: Optional[str] = None,
    semantic_api_key: Optional[str] = None
) -> Dict[str, int]:
    """Enrich citations in research_results.json format."""

    file_path = Path(file_path)
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return {'error': 1}

    # Load research results
    with open(file_path) as f:
        data = json.load(f)

    results = data.get('results', [])

    stats = {
        'total_citations': 0,
        'enriched': 0,
        'already_complete': 0,
        'failed': 0
    }

    async with OpenAlexClient(email=email) as openalex:
        async with SemanticScholarDOIClient(api_key=semantic_api_key) as semantic:
            for result in results:
                selected_citations = result.get('selected_citations', [])
                for citation in selected_citations:
                    # Citations are nested under 'paper' field
                    paper = citation.get('paper', {})
                    if not paper:
                        continue

                    stats['total_citations'] += 1

                    # Check if needs enrichment
                    if paper.get('citation_count') and paper.get('citation_count') > 0:
                        stats['already_complete'] += 1
                        continue

                    # Enrich citation
                    try:
                        await enrich_citation(paper, openalex, semantic)
                        # Check if enrichment succeeded by looking for enrichment_source
                        if paper.get('enrichment_source'):
                            stats['enriched'] += 1
                        else:
                            stats['failed'] += 1
                    except Exception as e:
                        logger.error(f"Failed to enrich citation: {e}")
                        stats['failed'] += 1

    # Save enriched data
    output_path = file_path.parent / f"{file_path.stem}_enriched.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved enriched data to {output_path}")
    logger.info(f"Stats: {stats}")
    return stats


async def enrich_all_batches(email: Optional[str] = None):
    """Enrich all completed batch files."""

    batch_files = [
        'batch_03_analysis_high.json',
        'batch_04_simulation_high.json',
        'batch_05_plant_high.json',
        'batch_06_interfaces_high.json',
        'batch_07_utils_high.json',
        'batch_08_other_high.json',
        'batch_09_medium_all.json',
    ]

    # Check .artifacts directory
    artifacts_dir = Path('.artifacts')
    if artifacts_dir.exists():
        batch_files = [str(artifacts_dir / f) for f in batch_files]

    total_stats = {
        'total_citations': 0,
        'enriched': 0,
        'already_complete': 0,
        'failed': 0
    }

    for batch_file in batch_files:
        if not Path(batch_file).exists():
            continue

        logger.info(f"\nProcessing {batch_file}...")
        stats = await enrich_batch_file(batch_file, email=email)

        for key in total_stats:
            total_stats[key] += stats.get(key, 0)

    logger.info("\n" + "="*80)
    logger.info("ENRICHMENT SUMMARY")
    logger.info("="*80)
    logger.info(f"Total citations: {total_stats['total_citations']}")
    logger.info(f"Already complete: {total_stats['already_complete']}")
    logger.info(f"Newly enriched: {total_stats['enriched']}")
    logger.info(f"Failed: {total_stats['failed']}")
    logger.info("="*80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Enrich citations with supplemental data')
    parser.add_argument('batch_file', nargs='?', help='Batch file to enrich')
    parser.add_argument('--all', action='store_true', help='Enrich all completed batches')
    parser.add_argument('--research-results', action='store_true', help='Enrich research_results.json')
    parser.add_argument('--email', help='Email for polite API access')
    parser.add_argument('--semantic-key', help='Semantic Scholar API key')

    args = parser.parse_args()

    if args.all:
        asyncio.run(enrich_all_batches(email=args.email))
    elif args.research_results:
        stats = asyncio.run(enrich_research_results(
            email=args.email,
            semantic_api_key=args.semantic_key
        ))
        print(f"\nEnrichment complete: {stats}")
    elif args.batch_file:
        stats = asyncio.run(enrich_batch_file(
            args.batch_file,
            email=args.email,
            semantic_api_key=args.semantic_key
        ))
        print(f"\nEnrichment complete: {stats}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
