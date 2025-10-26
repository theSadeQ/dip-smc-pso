# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/research_pipeline.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Automated research pipeline for citation discovery.

Orchestrates the complete workflow:
1. Load claims from inventory
2. Generate search queries
3. Search academic databases (Semantic Scholar, ArXiv, CrossRef)
4. Rank and filter results
5. Generate BibTeX entries
6. Save checkpoints for recovery

Usage:
    python research_pipeline.py --batch CRITICAL --max-claims 20
    python research_pipeline.py --resume  # Resume from checkpoint
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import asdict
import argparse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.api_clients import UnifiedResearchClient, Paper
from research.query_generator import QueryGenerator
from research.checkpoint_manager import CheckpointManager
from research.bibtex_generator import BibTeXGenerator

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# Research Pipeline
# ═══════════════════════════════════════════════════════════════════════════


class ResearchPipeline:
    """
    Main research pipeline orchestrator.

    Coordinates claim extraction → query generation → API search → BibTeX generation.
    """

    def __init__(
        self,
        semantic_scholar_key: Optional[str] = None,
        crossref_email: Optional[str] = None,
        checkpoint_dir: str = "artifacts/checkpoints",
        output_dir: str = "artifacts/research",
    ):
        """
        Initialize research pipeline.

        Args:
            semantic_scholar_key: Optional Semantic Scholar API key
            crossref_email: Email for CrossRef polite pool
            checkpoint_dir: Directory for checkpoints
            output_dir: Directory for research outputs
        """
        self.research_client = None
        self.semantic_scholar_key = semantic_scholar_key
        self.crossref_email = crossref_email

        self.query_gen = QueryGenerator()
        self.checkpoint_mgr = CheckpointManager(checkpoint_dir)
        self.bibtex_gen = BibTeXGenerator()

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ══════════════════════════════════════════════════════════════════════
    # Main Workflow
    # ══════════════════════════════════════════════════════════════════════

    async def run(
        self,
        claims_file: Path,
        priority_filter: Optional[str] = None,
        max_claims: Optional[int] = None,
        papers_per_claim: int = 5,
        citations_per_claim: int = 2,
    ) -> Dict[str, Any]:
        """
        Run complete research pipeline.

        Args:
            claims_file: Path to claims_inventory.json
            priority_filter: Filter by priority ('CRITICAL', 'HIGH', 'MEDIUM')
            max_claims: Maximum number of claims to process
            papers_per_claim: Max papers to find per claim
            citations_per_claim: Target citations per claim

        Returns:
            Research results summary
        """
        # Load claims
        claims = self._load_claims(claims_file, priority_filter, max_claims)
        logger.info(f"Loaded {len(claims)} claims for research")

        # Create session
        batch_name = priority_filter or "all_priorities"
        self.checkpoint_mgr.create_session(
            total_claims=len(claims), batch_name=batch_name
        )
        self.checkpoint_mgr.set_queued_claims([c["id"] for c in claims])

        # Initialize API client
        async with UnifiedResearchClient(
            semantic_scholar_key=self.semantic_scholar_key,
            crossref_email=self.crossref_email,
        ) as client:
            self.research_client = client

            # Process claims
            for claim in claims:
                await self._process_claim(
                    claim,
                    max_papers=papers_per_claim,
                    target_citations=citations_per_claim,
                )

                # Checkpoint if needed
                if self.checkpoint_mgr.should_checkpoint():
                    self.checkpoint_mgr.save_checkpoint()

        # Final checkpoint
        self.checkpoint_mgr.save_checkpoint()

        # Generate outputs
        results = self._generate_outputs()

        return results

    async def resume(
        self,
        papers_per_claim: int = 5,
        citations_per_claim: int = 2,
    ) -> Dict[str, Any]:
        """
        Resume from last checkpoint.

        Args:
            papers_per_claim: Max papers to find per claim
            citations_per_claim: Target citations per claim

        Returns:
            Research results summary
        """
        if not self.checkpoint_mgr.can_resume():
            raise ValueError("No checkpoint found to resume from")

        checkpoint = self.checkpoint_mgr.load_latest_checkpoint()
        logger.info(f"Resuming from checkpoint: {checkpoint.checkpoint_id}")

        # Get remaining claims
        remaining_claim_ids = self.checkpoint_mgr.get_remaining_claims()
        if not remaining_claim_ids:
            logger.info("All claims already processed")
            return self._generate_outputs()

        # Load full claim data (would need claims_inventory.json path)
        # For now, log and continue
        logger.info(f"Resuming with {len(remaining_claim_ids)} claims remaining")

        # Continue processing
        # (Implementation similar to run() but with remaining claims)

        return self._generate_outputs()

    # ══════════════════════════════════════════════════════════════════════
    # Claim Processing
    # ══════════════════════════════════════════════════════════════════════

    async def _process_claim(
        self, claim: Dict, max_papers: int, target_citations: int
    ) -> None:
        """
        Process a single claim: generate queries → search → rank → select.

        Args:
            claim: Claim dictionary
            max_papers: Maximum papers to find
            target_citations: Number of citations to select
        """
        claim_id = claim["id"]
        claim_text = claim.get("description") or claim.get("claim_text") or claim.get("statement") or claim.get("text", "")
        start_time = time.time()

        try:
            logger.info(f"Processing {claim_id}: {claim_text[:60]}...")

            # Generate search queries
            queries = self.query_gen.generate(claim_text, max_queries=3)
            logger.debug(f"Generated {len(queries)} queries for {claim_id}")

            # Search for papers
            all_papers = []
            for query in queries[:2]:  # Use top 2 queries
                papers = await self.research_client.search(
                    query.text, max_results=max_papers
                )
                all_papers.extend(papers)

            # Deduplicate and rank
            unique_papers = self._deduplicate_papers(all_papers)
            ranked_papers = self._rank_papers(unique_papers, claim_text)

            # Select top citations
            selected_papers = ranked_papers[:target_citations]

            # Generate BibTeX
            topic = self._infer_topic(claim)
            bibtex_entries = self.bibtex_gen.generate_entries(
                selected_papers, topic=topic
            )

            # Record result
            processing_time = time.time() - start_time
            self.checkpoint_mgr.record_result(
                claim_id=claim_id,
                claim_text=claim_text,
                queries=[q.text for q in queries],
                papers=[self._paper_to_dict(p) for p in ranked_papers[:max_papers]],
                citations=[entry for entry in bibtex_entries],
                processing_time=processing_time,
                status="success" if len(selected_papers) > 0 else "partial",
            )

            logger.info(
                f"Completed {claim_id}: {len(selected_papers)} citations in {processing_time:.2f}s"
            )

        except Exception as e:
            logger.error(f"Error processing {claim_id}: {e}", exc_info=True)
            processing_time = time.time() - start_time
            self.checkpoint_mgr.record_result(
                claim_id=claim_id,
                claim_text=claim_text,
                queries=[],
                papers=[],
                citations=[],
                processing_time=processing_time,
                status="failed",
                error=str(e),
            )

    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers based on title similarity."""
        from difflib import SequenceMatcher

        unique = []
        for paper in papers:
            is_duplicate = False
            for existing in unique:
                similarity = SequenceMatcher(
                    None,
                    paper.title.lower().strip(),
                    existing.title.lower().strip(),
                ).ratio()

                if similarity > 0.85:
                    # Keep the one with more citations
                    if paper.citation_count > existing.citation_count:
                        unique.remove(existing)
                        unique.append(paper)
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(paper)

        return unique

    def _rank_papers(self, papers: List[Paper], claim_text: str) -> List[Paper]:
        """
        Rank papers by relevance to claim.

        Scoring factors:
        - Title relevance to claim (HIGH WEIGHT)
        - Domain filtering (control theory vs other domains)
        - Citation count (REDUCED WEIGHT)
        - Recency (newer = better)
        - Venue prestige (journal > conference > misc)
        """
        scored_papers = []

        for paper in papers:
            score = 0.0

            # Domain filtering (CRITICAL)
            if not self._is_control_theory_paper(paper):
                score -= 20.0  # Heavy penalty for wrong domain

            # Title relevance (INCREASED WEIGHT)
            claim_keywords = set(claim_text.lower().split())
            title_keywords = set(paper.title.lower().split())
            overlap = len(claim_keywords & title_keywords)
            score += overlap * 3.0  # Was 0.5, now 3.0

            # Abstract relevance (if available)
            if paper.abstract:
                abstract_keywords = set(paper.abstract.lower().split())
                abstract_overlap = len(claim_keywords & abstract_keywords)
                score += min(abstract_overlap * 0.5, 5.0)  # Cap at 5.0

            # Citation count (REDUCED WEIGHT - logarithmic scaling)
            import math
            score += math.log(paper.citation_count + 1) * 0.5  # Was 2.0, now 0.5

            # Recency bonus
            if paper.year and paper.year >= 2015:
                score += (paper.year - 2015) * 0.3  # Was 0.5, now 0.3

            # Venue prestige
            if paper.venue:
                venue_lower = paper.venue.lower()
                if any(
                    kw in venue_lower for kw in ["journal", "transactions", "letters"]
                ):
                    score += 2.0  # Was 3.0, now 2.0
                elif any(kw in venue_lower for kw in ["conference", "symposium"]):
                    score += 1.0  # Was 2.0, now 1.0

            # DOI availability (CRITICAL for citation quality)
            if paper.doi:
                score += 5.0  # Strong bonus for papers with DOIs

            scored_papers.append((score, paper))

        # Sort by score (descending)
        scored_papers.sort(key=lambda x: x[0], reverse=True)

        return [paper for score, paper in scored_papers]

    def _is_control_theory_paper(self, paper: Paper) -> bool:
        """
        Check if paper is control theory vs other domains.

        Returns:
            True if paper is control theory, False otherwise
        """
        # Control theory keywords
        control_keywords = {
            'control', 'controller', 'sliding mode', 'lyapunov',
            'stability', 'feedback', 'regulation', 'tracking',
            'adaptive', 'robust', 'nonlinear control', 'pid',
            'mpc', 'model predictive', 'state feedback',
            'sliding surface', 'reaching law', 'switching',
            'gain', 'convergence', 'stabilization'
        }

        # Non-control domain keywords (penalize these)
        fluid_keywords = {
            'turbulent', 'reynolds number', 'flow', 'fluid',
            'boundary layer flow', 'navier-stokes', 'vortex',
            'particle-fluid', 'hypersonic', 'aerodynamic'
        }

        math_only_keywords = {
            'orbifold', 'algebraic geometry', 'topology',
            'riemannian', 'manifold', 'homology'
        }

        # Combine title and abstract
        text = (paper.title + ' ' + (paper.abstract or '')).lower()

        # Heavy penalty for fluid dynamics or pure math
        if any(kw in text for kw in fluid_keywords):
            return False
        if any(kw in text for kw in math_only_keywords):
            return False

        # Require at least one control keyword
        return any(kw in text for kw in control_keywords)

    # ══════════════════════════════════════════════════════════════════════
    # Output Generation
    # ══════════════════════════════════════════════════════════════════════

    def _generate_outputs(self) -> Dict[str, Any]:
        """Generate final research outputs."""
        # Collect all BibTeX entries
        all_entries = []
        for result in self.checkpoint_mgr.results:
            if result.selected_citations:
                all_entries.extend(result.selected_citations)

        # Save BibTeX file
        bibtex_path = self.output_dir / "enhanced_bibliography.bib"
        self.bibtex_gen.save_bibliography(all_entries, bibtex_path)

        # Save research results JSON
        results_path = self.output_dir / "research_results.json"
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "session_id": self.checkpoint_mgr.session_id,
                    "progress": asdict(self.checkpoint_mgr.progress),
                    "results": [asdict(r) for r in self.checkpoint_mgr.results],
                },
                f,
                indent=2,
            )

        # Generate summary
        summary = {
            "session_id": self.checkpoint_mgr.session_id,
            "total_claims": self.checkpoint_mgr.progress.total_claims,
            "claims_processed": self.checkpoint_mgr.progress.claims_processed,
            "claims_successful": self.checkpoint_mgr.progress.claims_successful,
            "citations_generated": len(all_entries),
            "bibtex_file": str(bibtex_path),
            "results_file": str(results_path),
        }

        logger.info(f"Research complete: {len(all_entries)} citations generated")
        return summary

    # ══════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ══════════════════════════════════════════════════════════════════════

    def _load_claims(
        self,
        claims_file: Path,
        priority_filter: Optional[str],
        max_claims: Optional[int],
    ) -> List[Dict]:
        """Load claims from inventory file."""
        with open(claims_file, "r", encoding="utf-8") as f:
            inventory = json.load(f)

        claims = inventory["claims"]

        # Filter by priority
        if priority_filter:
            claims = [c for c in claims if c["priority"] == priority_filter]

        # Limit claims
        if max_claims:
            claims = claims[:max_claims]

        return claims

    def _infer_topic(self, claim: Dict) -> str:
        """Infer topic prefix from claim metadata."""
        text = claim.get("text", "").lower()

        if "smc" in text or "sliding mode" in text:
            return "smc"
        elif "pso" in text or "particle swarm" in text:
            return "pso"
        elif "pendulum" in text or "dip" in text:
            return "dip"
        else:
            return "ref"

    def _paper_to_dict(self, paper: Paper) -> Dict:
        """Convert Paper object to dictionary."""
        return {
            "title": paper.title,
            "authors": paper.authors,
            "year": paper.year,
            "doi": paper.doi,
            "url": paper.url,
            "venue": paper.venue,
            "citation_count": paper.citation_count,
            "source": paper.source,
        }


# ═══════════════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════════════


async def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automated research pipeline for citation discovery"
    )
    parser.add_argument(
        "--claims-file",
        type=Path,
        default=Path("artifacts/claims_inventory.json"),
        help="Path to claims inventory JSON",
    )
    parser.add_argument(
        "--priority",
        choices=["CRITICAL", "HIGH", "MEDIUM"],
        help="Filter claims by priority",
    )
    parser.add_argument(
        "--max-claims",
        type=int,
        help="Maximum number of claims to process",
    )
    parser.add_argument(
        "--papers-per-claim",
        type=int,
        default=5,
        help="Maximum papers to find per claim",
    )
    parser.add_argument(
        "--citations-per-claim",
        type=int,
        default=2,
        help="Target number of citations per claim",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last checkpoint",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Initialize pipeline
    pipeline = ResearchPipeline(
        crossref_email="research@example.com"  # Replace with actual email
    )

    # Run pipeline
    try:
        if args.resume:
            results = await pipeline.resume(
                papers_per_claim=args.papers_per_claim,
                citations_per_claim=args.citations_per_claim,
            )
        else:
            results = await pipeline.run(
                claims_file=args.claims_file,
                priority_filter=args.priority,
                max_claims=args.max_claims,
                papers_per_claim=args.papers_per_claim,
                citations_per_claim=args.citations_per_claim,
            )

        # Print summary
        print("\n" + "=" * 70)
        print("RESEARCH PIPELINE COMPLETE")
        print("=" * 70)
        print(f"Session ID:          {results['session_id']}")
        print(f"Claims Processed:    {results['claims_processed']} / {results['total_claims']}")
        print(f"Successful:          {results['claims_successful']}")
        print(f"Citations Generated: {results['citations_generated']}")
        print("\nOutputs:")
        print(f"  BibTeX:  {results['bibtex_file']}")
        print(f"  Results: {results['results_file']}")
        print("=" * 70)

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        pipeline.checkpoint_mgr.save_checkpoint()
        print("\n✓ Progress saved to checkpoint. Use --resume to continue.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
