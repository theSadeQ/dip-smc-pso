# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/api_clients.py
# ═══════════════════════════════════════════════════════════════════════════
"""
API clients for academic research databases.

Provides unified interface to Semantic Scholar, ArXiv, and CrossRef APIs
with rate limiting, exponential backoff, and checkpoint recovery.

Rate Limits:
- Semantic Scholar: 100 requests per 5 minutes
- ArXiv: 3 requests per second
- CrossRef: Polite pool (50 req/sec with email)
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import aiohttp
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class Paper:
    """Academic paper metadata."""

    title: str
    authors: List[str]
    year: Optional[int]
    doi: Optional[str]
    url: Optional[str]
    abstract: Optional[str]
    venue: Optional[str]
    citation_count: int = 0
    arxiv_id: Optional[str] = None
    source: str = ""  # 'semantic_scholar', 'arxiv', 'crossref'
    relevance_score: float = 0.0

    def to_bibtex_dict(self) -> Dict[str, str]:
        """Convert to BibTeX-compatible dictionary."""
        entry = {
            "title": self.title,
            "author": " and ".join(self.authors) if self.authors else "",
            "year": str(self.year) if self.year else "",
        }

        if self.doi:
            entry["doi"] = self.doi
        if self.url:
            entry["url"] = self.url
        if self.venue:
            entry["journal"] = self.venue

        return entry


@dataclass
class RateLimiter:
    """Token bucket rate limiter with exponential backoff."""

    requests_per_period: int
    period_seconds: float
    max_retries: int = 5

    tokens: float = field(init=False)
    last_refill: float = field(init=False)

    def __post_init__(self):
        self.tokens = self.requests_per_period
        self.last_refill = time.time()

    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        while True:
            now = time.time()
            elapsed = now - self.last_refill

            # Refill tokens based on elapsed time
            refill_amount = elapsed * (self.requests_per_period / self.period_seconds)
            self.tokens = min(self.requests_per_period, self.tokens + refill_amount)
            self.last_refill = now

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return

            # Wait until next token available
            wait_time = (1.0 - self.tokens) * (
                self.period_seconds / self.requests_per_period
            )
            logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)


# ═══════════════════════════════════════════════════════════════════════════
# Semantic Scholar API Client
# ═══════════════════════════════════════════════════════════════════════════


class SemanticScholarClient:
    """
    Client for Semantic Scholar API.

    Rate Limit: 100 requests per 5 minutes (free tier)
    Documentation: https://api.semanticscholar.org/

    Usage:
        async with SemanticScholarClient() as client:
            papers = await client.search("sliding mode control")
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Semantic Scholar client.

        Args:
            api_key: Optional API key for higher rate limits
        """
        self.api_key = api_key
        self.rate_limiter = RateLimiter(
            requests_per_period=100, period_seconds=300  # 100 req / 5 min
        )
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search(
        self, query: str, limit: int = 10, fields: Optional[List[str]] = None
    ) -> List[Paper]:
        """
        Search for papers by query string.

        Args:
            query: Search query
            limit: Maximum number of results
            fields: Fields to retrieve (default: title, authors, year, abstract)

        Returns:
            List of Paper objects
        """
        if fields is None:
            fields = [
                "title",
                "authors",
                "year",
                "abstract",
                "citationCount",
                "venue",
                "externalIds",
                "url",
            ]

        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/paper/search"
        params = {"query": query, "limit": limit, "fields": ",".join(fields)}

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        try:
            async with self.session.get(url, params=params, headers=headers) as resp:
                if resp.status == 429:
                    logger.warning("Rate limit exceeded, backing off...")
                    await asyncio.sleep(60)  # Wait 1 minute
                    return await self.search(query, limit, fields)

                resp.raise_for_status()
                data = await resp.json()

                papers = []
                for item in data.get("data", []):
                    paper = Paper(
                        title=item.get("title", ""),
                        authors=[
                            author.get("name", "")
                            for author in item.get("authors", [])
                        ],
                        year=item.get("year"),
                        abstract=item.get("abstract"),
                        venue=item.get("venue"),
                        citation_count=item.get("citationCount", 0),
                        doi=item.get("externalIds", {}).get("DOI"),
                        url=item.get("url"),
                        source="semantic_scholar",
                    )
                    papers.append(paper)

                logger.info(f"Semantic Scholar: Found {len(papers)} papers for '{query}'")
                return papers

        except aiohttp.ClientError as e:
            logger.error(f"Semantic Scholar API error: {e}")
            return []


# ═══════════════════════════════════════════════════════════════════════════
# ArXiv API Client
# ═══════════════════════════════════════════════════════════════════════════


class ArXivClient:
    """
    Client for ArXiv API.

    Rate Limit: 3 requests per second (recommended)
    Documentation: https://arxiv.org/help/api

    Usage:
        async with ArXivClient() as client:
            papers = await client.search("particle swarm optimization")
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self):
        self.rate_limiter = RateLimiter(
            requests_per_period=3, period_seconds=1.0  # 3 req / second
        )
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance",
        sort_order: str = "descending",
    ) -> List[Paper]:
        """
        Search ArXiv for papers.

        Args:
            query: Search query (use ArXiv query format)
            max_results: Maximum number of results
            sort_by: Sort criterion ('relevance', 'lastUpdatedDate', 'submittedDate')
            sort_order: 'ascending' or 'descending'

        Returns:
            List of Paper objects
        """
        await self.rate_limiter.acquire()

        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        try:
            async with self.session.get(self.BASE_URL, params=params) as resp:
                resp.raise_for_status()
                text = await resp.text()

                # Parse Atom XML response
                papers = self._parse_arxiv_response(text)
                logger.info(f"ArXiv: Found {len(papers)} papers for '{query}'")
                return papers

        except aiohttp.ClientError as e:
            logger.error(f"ArXiv API error: {e}")
            return []

    def _parse_arxiv_response(self, xml_text: str) -> List[Paper]:
        """Parse ArXiv Atom XML response."""
        import xml.etree.ElementTree as ET

        papers = []
        root = ET.fromstring(xml_text)

        # Define namespaces
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }

        for entry in root.findall("atom:entry", ns):
            title_elem = entry.find("atom:title", ns)
            title = title_elem.text.strip() if title_elem is not None else ""

            authors = []
            for author in entry.findall("atom:author", ns):
                name_elem = author.find("atom:name", ns)
                if name_elem is not None:
                    authors.append(name_elem.text)

            published_elem = entry.find("atom:published", ns)
            year = None
            if published_elem is not None:
                year_str = published_elem.text[:4]
                year = int(year_str) if year_str.isdigit() else None

            abstract_elem = entry.find("atom:summary", ns)
            abstract = abstract_elem.text.strip() if abstract_elem is not None else None

            id_elem = entry.find("atom:id", ns)
            arxiv_id = id_elem.text.split("/")[-1] if id_elem is not None else None

            link_elem = entry.find("atom:link[@title='pdf']", ns)
            url = link_elem.get("href") if link_elem is not None else None

            # ArXiv doesn't provide DOI or citation counts directly
            paper = Paper(
                title=title,
                authors=authors,
                year=year,
                abstract=abstract,
                arxiv_id=arxiv_id,
                url=url,
                doi=None,
                venue="arXiv",
                source="arxiv",
            )
            papers.append(paper)

        return papers


# ═══════════════════════════════════════════════════════════════════════════
# CrossRef API Client
# ═══════════════════════════════════════════════════════════════════════════


class CrossRefClient:
    """
    Client for CrossRef API.

    Rate Limit: Polite pool (50 req/sec with email in User-Agent)
    Documentation: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

    Usage:
        async with CrossRefClient(email="your@email.com") as client:
            papers = await client.search("nonlinear control")
    """

    BASE_URL = "https://api.crossref.org"

    def __init__(self, email: Optional[str] = None):
        """
        Initialize CrossRef client.

        Args:
            email: Email for polite pool (gets higher rate limit)
        """
        self.email = email
        self.rate_limiter = RateLimiter(
            requests_per_period=50, period_seconds=1.0  # 50 req / second (polite)
        )
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

    async def search(self, query: str, rows: int = 10) -> List[Paper]:
        """
        Search CrossRef for papers.

        Args:
            query: Search query
            rows: Number of results

        Returns:
            List of Paper objects
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/works"
        params = {"query": query, "rows": rows, "select": "title,author,published,DOI,URL,abstract,container-title"}

        try:
            async with self.session.get(url, params=params) as resp:
                resp.raise_for_status()
                data = await resp.json()

                papers = []
                for item in data.get("message", {}).get("items", []):
                    # Extract title
                    title_list = item.get("title", [])
                    title = title_list[0] if title_list else ""

                    # Extract authors
                    authors = []
                    for author in item.get("author", []):
                        given = author.get("given", "")
                        family = author.get("family", "")
                        name = f"{given} {family}".strip()
                        if name:
                            authors.append(name)

                    # Extract year
                    published = item.get("published", {}).get("date-parts", [[]])[0]
                    year = published[0] if published else None

                    # Extract venue
                    venue_list = item.get("container-title", [])
                    venue = venue_list[0] if venue_list else None

                    paper = Paper(
                        title=title,
                        authors=authors,
                        year=year,
                        doi=item.get("DOI"),
                        url=item.get("URL"),
                        abstract=item.get("abstract"),
                        venue=venue,
                        source="crossref",
                    )
                    papers.append(paper)

                logger.info(f"CrossRef: Found {len(papers)} papers for '{query}'")
                return papers

        except aiohttp.ClientError as e:
            logger.error(f"CrossRef API error: {e}")
            return []

    async def get_by_doi(self, doi: str) -> Optional[Paper]:
        """
        Retrieve paper metadata by DOI.

        Args:
            doi: DOI identifier

        Returns:
            Paper object or None
        """
        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/works/{doi}"

        try:
            async with self.session.get(url) as resp:
                if resp.status == 404:
                    logger.warning(f"DOI not found: {doi}")
                    return None

                resp.raise_for_status()
                data = await resp.json()
                item = data.get("message", {})

                # Same parsing as search()
                title_list = item.get("title", [])
                title = title_list[0] if title_list else ""

                authors = []
                for author in item.get("author", []):
                    given = author.get("given", "")
                    family = author.get("family", "")
                    name = f"{given} {family}".strip()
                    if name:
                        authors.append(name)

                published = item.get("published", {}).get("date-parts", [[]])[0]
                year = published[0] if published else None

                venue_list = item.get("container-title", [])
                venue = venue_list[0] if venue_list else None

                return Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    doi=item.get("DOI"),
                    url=item.get("URL"),
                    abstract=item.get("abstract"),
                    venue=venue,
                    source="crossref",
                )

        except aiohttp.ClientError as e:
            logger.error(f"CrossRef DOI lookup error: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════
# OpenAlex API Client (for enrichment)
# ═══════════════════════════════════════════════════════════════════════════


class OpenAlexClient:
    """
    Client for OpenAlex API - free, comprehensive academic database.

    Provides: citation counts, abstracts, open access links
    Rate Limit: 10 requests/second (no auth), 100 req/sec (with email)
    Documentation: https://docs.openalex.org/

    Usage:
        async with OpenAlexClient() as client:
            paper = await client.get_by_doi("10.1109/TAC.2003.809149")
    """

    BASE_URL = "https://api.openalex.org"

    def __init__(self, email: Optional[str] = None):
        """
        Initialize OpenAlex client.

        Args:
            email: Email for polite pool (gets higher rate limit)
        """
        self.email = email
        self.rate_limiter = RateLimiter(
            requests_per_period=10, period_seconds=1.0  # 10 req / second
        )
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

    async def get_by_doi(self, doi: str) -> Optional[Paper]:
        """
        Lookup paper by DOI and return enriched metadata.

        Args:
            doi: DOI identifier

        Returns:
            Paper object with citation counts and abstract, or None
        """
        if not doi:
            return None

        await self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/works/https://doi.org/{doi}"

        try:
            async with self.session.get(url) as resp:
                if resp.status == 404:
                    return None

                resp.raise_for_status()
                data = await resp.json()

                # Extract enriched data
                title = data.get("title", "")

                # Authors
                authors = []
                for authorship in data.get("authorships", []):
                    author = authorship.get("author", {})
                    name = author.get("display_name", "")
                    if name:
                        authors.append(name)

                # Year
                year = data.get("publication_year")

                # Abstract (from inverted index)
                abstract = self._extract_abstract(data)

                # Venue
                venue = None
                primary_location = data.get("primary_location", {})
                source = primary_location.get("source", {})
                venue = source.get("display_name")

                # Open access URL
                oa_url = None
                if primary_location.get("is_oa"):
                    oa_url = primary_location.get("pdf_url") or primary_location.get("landing_page_url")

                paper = Paper(
                    title=title,
                    authors=authors,
                    year=year,
                    doi=doi,
                    url=data.get("doi"),
                    abstract=abstract,
                    venue=venue,
                    citation_count=data.get("cited_by_count", 0),
                    source="openalex",
                )

                logger.debug(f"OpenAlex: Enriched DOI {doi} - {paper.citation_count} citations")
                return paper

        except Exception as e:
            logger.debug(f"OpenAlex lookup failed for {doi}: {e}")
            return None

    def _extract_abstract(self, data: Dict) -> Optional[str]:
        """Extract abstract from OpenAlex inverted index format."""
        abstract_inv = data.get("abstract_inverted_index")
        if not abstract_inv:
            return None

        # Reconstruct abstract from inverted index
        words = {}
        for word, positions in abstract_inv.items():
            for pos in positions:
                words[pos] = word

        if words:
            return " ".join(words[i] for i in sorted(words.keys()))
        return None


# ═══════════════════════════════════════════════════════════════════════════
# Unified Research Client
# ═══════════════════════════════════════════════════════════════════════════


class UnifiedResearchClient:
    """
    Unified client that searches across multiple academic databases.

    Orchestrates parallel searches and merges results with deduplication.

    Usage:
        async with UnifiedResearchClient() as client:
            papers = await client.search("super-twisting algorithm", max_results=20)
    """

    def __init__(
        self,
        semantic_scholar_key: Optional[str] = None,
        crossref_email: Optional[str] = None,
        auto_enrich: bool = True,
    ):
        """
        Initialize unified research client.

        Args:
            semantic_scholar_key: Optional Semantic Scholar API key
            crossref_email: Email for CrossRef polite pool
            auto_enrich: Automatically enrich papers with citation counts (default: True)
        """
        self.semantic_scholar = SemanticScholarClient(api_key=semantic_scholar_key)
        self.arxiv = ArXivClient()
        self.crossref = CrossRefClient(email=crossref_email)
        self.openalex = OpenAlexClient(email=crossref_email)
        self.auto_enrich = auto_enrich

    async def __aenter__(self):
        await self.semantic_scholar.__aenter__()
        await self.arxiv.__aenter__()
        await self.crossref.__aenter__()
        await self.openalex.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.semantic_scholar.__aexit__(exc_type, exc_val, exc_tb)
        await self.arxiv.__aexit__(exc_type, exc_val, exc_tb)
        await self.crossref.__aexit__(exc_type, exc_val, exc_tb)
        await self.openalex.__aexit__(exc_type, exc_val, exc_tb)

    async def search(
        self, query: str, max_results: int = 10, sources: Optional[List[str]] = None
    ) -> List[Paper]:
        """
        Search across multiple databases in parallel.

        Args:
            query: Search query
            max_results: Maximum results per source
            sources: List of sources to search (default: all)

        Returns:
            Deduplicated list of papers, sorted by relevance
        """
        if sources is None:
            sources = ["semantic_scholar", "arxiv", "crossref"]

        tasks = []
        if "semantic_scholar" in sources:
            tasks.append(self.semantic_scholar.search(query, limit=max_results))
        if "arxiv" in sources:
            tasks.append(self.arxiv.search(query, max_results=max_results))
        if "crossref" in sources:
            tasks.append(self.crossref.search(query, rows=max_results))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results
        all_papers = []
        for result in results:
            if isinstance(result, list):
                all_papers.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Search failed: {result}")

        # Deduplicate by title similarity
        unique_papers = self._deduplicate(all_papers)

        # Auto-enrich papers with citation counts if enabled
        if self.auto_enrich:
            unique_papers = await self._enrich_papers(unique_papers)

        # Rank by citation count and recency
        unique_papers.sort(
            key=lambda p: (p.citation_count, p.year or 0), reverse=True
        )

        logger.info(
            f"Unified search: {len(all_papers)} total → {len(unique_papers)} unique"
        )
        return unique_papers[:max_results]

    def _deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers based on title similarity."""
        from difflib import SequenceMatcher

        unique = []
        for paper in papers:
            is_duplicate = False
            for existing in unique:
                # Compare titles (case-insensitive, normalized)
                similarity = SequenceMatcher(
                    None,
                    paper.title.lower().strip(),
                    existing.title.lower().strip(),
                ).ratio()

                if similarity > 0.85:  # 85% similarity threshold
                    # Keep the one with more metadata
                    if paper.citation_count > existing.citation_count:
                        unique.remove(existing)
                        unique.append(paper)
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(paper)

        return unique


# ═══════════════════════════════════════════════════════════════════════════
# Example Usage
# ═══════════════════════════════════════════════════════════════════════════


async def main():
    """Example usage of research clients."""
    logging.basicConfig(level=logging.INFO)

    # Test unified client
    async with UnifiedResearchClient(crossref_email="research@example.com") as client:
        papers = await client.search("sliding mode control", max_results=5)

        print(f"\nFound {len(papers)} unique papers:\n")
        for i, paper in enumerate(papers, 1):
            print(f"{i}. {paper.title}")
            print(f"   Authors: {', '.join(paper.authors[:3])}...")
            print(f"   Year: {paper.year}, Citations: {paper.citation_count}")
            print(f"   Source: {paper.source}, DOI: {paper.doi}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
