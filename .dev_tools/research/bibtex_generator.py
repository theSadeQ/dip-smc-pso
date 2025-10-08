# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/bibtex_generator.py
# ═══════════════════════════════════════════════════════════════════════════
"""
BibTeX generation for academic citations.

Converts Paper objects from research APIs into IEEE-formatted BibTeX entries.
Handles deduplication, key generation, and validation.

Key Naming Convention:
    topic_authorYear_shortTitle

Examples:
    smc_slotine1991_applied_nonlinear_control
    pso_kennedy1995_particle_swarm
    dip_khalil2002_nonlinear_systems
"""

import re
from typing import List, Dict, Optional, Set
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# Import Paper from api_clients
try:
    from .api_clients import Paper
except ImportError:
    # Fallback for standalone testing
    from dataclasses import dataclass

    @dataclass
    class Paper:
        title: str
        authors: List[str]
        year: Optional[int]
        doi: Optional[str]
        url: Optional[str]
        abstract: Optional[str]
        venue: Optional[str]
        citation_count: int = 0
        arxiv_id: Optional[str] = None
        source: str = ""


# ═══════════════════════════════════════════════════════════════════════════
# BibTeX Entry Templates
# ═══════════════════════════════════════════════════════════════════════════


IEEE_ARTICLE_TEMPLATE = """@article{{{key},
    author = {{{authors}}},
    title = {{{{{title}}}}},
    journal = {{{journal}}},
    year = {{{year}}},{doi}{url}
}}"""

IEEE_INPROCEEDINGS_TEMPLATE = """@inproceedings{{{key},
    author = {{{authors}}},
    title = {{{{{title}}}}},
    booktitle = {{{booktitle}}},
    year = {{{year}}},{doi}{url}
}}"""

IEEE_BOOK_TEMPLATE = """@book{{{key},
    author = {{{authors}}},
    title = {{{{{title}}}}},
    publisher = {{{publisher}}},
    year = {{{year}}},{doi}{url}
}}"""

IEEE_MISC_TEMPLATE = """@misc{{{key},
    author = {{{authors}}},
    title = {{{{{title}}}}},
    howpublished = {{{howpublished}}},
    year = {{{year}}},{doi}{url}
}}"""


# ═══════════════════════════════════════════════════════════════════════════
# BibTeX Generator
# ═══════════════════════════════════════════════════════════════════════════


class BibTeXGenerator:
    """
    Generate IEEE-formatted BibTeX entries from Paper objects.

    Usage:
        gen = BibTeXGenerator()
        entries = gen.generate_entries(papers, topic="smc")
        bibtex_text = gen.format_bibliography(entries)
    """

    # Topic prefixes for citation keys
    TOPIC_PREFIXES = {
        "sliding mode": "smc",
        "super-twisting": "smc",
        "adaptive control": "smc",
        "particle swarm": "pso",
        "PSO": "pso",
        "optimization": "pso",
        "inverted pendulum": "dip",
        "double inverted pendulum": "dip",
        "DIP": "dip",
        "lyapunov": "control",
        "stability": "control",
        "control theory": "control",
        "fault detection": "fdi",
        "FDI": "fdi",
        "numerical methods": "num",
        "software": "soft",
    }

    def __init__(self):
        """Initialize BibTeX generator."""
        self.generated_keys: Set[str] = set()

    # ══════════════════════════════════════════════════════════════════════
    # Entry Generation
    # ══════════════════════════════════════════════════════════════════════

    def generate_entries(
        self, papers: List[Paper], topic: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generate BibTeX entries for a list of papers.

        Args:
            papers: List of Paper objects
            topic: Topic for citation key prefix (e.g., 'smc', 'pso')

        Returns:
            List of BibTeX entry dictionaries
        """
        entries = []

        for paper in papers:
            entry = self.paper_to_bibtex(paper, topic=topic)
            if entry:
                entries.append(entry)

        logger.info(f"Generated {len(entries)} BibTeX entries")
        return entries

    def paper_to_bibtex(
        self, paper: Paper, topic: Optional[str] = None
    ) -> Optional[Dict[str, str]]:
        """
        Convert a Paper object to a BibTeX entry.

        Args:
            paper: Paper object
            topic: Optional topic for key prefix

        Returns:
            Dictionary with 'key' and 'entry' fields
        """
        # Determine entry type
        entry_type = self._determine_entry_type(paper)

        # Generate citation key
        key = self._generate_key(paper, topic=topic)

        # Build entry fields
        fields = {
            "key": key,
            "authors": self._format_authors(paper.authors),
            "title": self._clean_title(paper.title),
            "year": str(paper.year) if paper.year else "n.d.",
        }

        # Add type-specific fields
        if entry_type == "article":
            fields["journal"] = paper.venue or "arXiv" if paper.arxiv_id else "Unknown"
        elif entry_type == "inproceedings":
            fields["booktitle"] = paper.venue or "Unknown Conference"
        elif entry_type == "book":
            fields["publisher"] = "Unknown Publisher"  # Would need additional data
        elif entry_type == "misc":
            if paper.arxiv_id:
                fields["howpublished"] = f"arXiv:{paper.arxiv_id}"
            else:
                fields["howpublished"] = "Online"

        # Add DOI and URL
        fields["doi"] = f"\n    doi = {{{paper.doi}}}," if paper.doi else ""
        fields["url"] = f"\n    url = {{{paper.url}}}," if paper.url else ""

        # Select template and format
        template = self._get_template(entry_type)
        entry_text = template.format(**fields)

        return {"key": key, "entry": entry_text, "type": entry_type, "paper": paper}

    def _determine_entry_type(self, paper: Paper) -> str:
        """Determine BibTeX entry type from paper metadata."""
        if not paper.venue:
            return "misc"

        venue_lower = paper.venue.lower()

        # Conference patterns
        conf_keywords = [
            "conference",
            "symposium",
            "workshop",
            "proceedings",
            "international",
        ]
        if any(kw in venue_lower for kw in conf_keywords):
            return "inproceedings"

        # Journal patterns
        journal_keywords = ["journal", "transactions", "letters", "magazine"]
        if any(kw in venue_lower for kw in journal_keywords):
            return "article"

        # Book patterns
        book_keywords = ["book", "handbook", "monograph", "press"]
        if any(kw in venue_lower for kw in book_keywords):
            return "book"

        # Default
        return "article"

    def _get_template(self, entry_type: str) -> str:
        """Get BibTeX template for entry type."""
        templates = {
            "article": IEEE_ARTICLE_TEMPLATE,
            "inproceedings": IEEE_INPROCEEDINGS_TEMPLATE,
            "book": IEEE_BOOK_TEMPLATE,
            "misc": IEEE_MISC_TEMPLATE,
        }
        return templates.get(entry_type, IEEE_MISC_TEMPLATE)

    # ══════════════════════════════════════════════════════════════════════
    # Citation Key Generation
    # ══════════════════════════════════════════════════════════════════════

    def _generate_key(self, paper: Paper, topic: Optional[str] = None) -> str:
        """
        Generate citation key following convention: topic_authorYear_shortTitle

        Args:
            paper: Paper object
            topic: Topic prefix (e.g., 'smc', 'pso')

        Returns:
            Citation key (ASCII, snake_case)
        """
        # Determine topic prefix
        if not topic:
            topic = self._infer_topic(paper)

        # Extract first author last name
        author_name = self._extract_author_name(paper.authors)

        # Extract year
        year = str(paper.year) if paper.year else "nd"

        # Extract short title
        short_title = self._extract_short_title(paper.title)

        # Combine
        base_key = f"{topic}_{author_name}{year}_{short_title}"

        # Ensure uniqueness
        key = base_key
        suffix = 2
        while key in self.generated_keys:
            key = f"{base_key}_{suffix}"
            suffix += 1

        self.generated_keys.add(key)
        return key

    def _infer_topic(self, paper: Paper) -> str:
        """Infer topic from paper title and abstract."""
        text = (paper.title + " " + (paper.abstract or "")).lower()

        for keyword, prefix in self.TOPIC_PREFIXES.items():
            if keyword.lower() in text:
                return prefix

        return "ref"  # Default prefix

    def _extract_author_name(self, authors: List[str]) -> str:
        """Extract first author's last name."""
        if not authors:
            return "unknown"

        # Get first author
        first_author = authors[0]

        # Extract last name (assume "First Last" or "Last, First" format)
        if "," in first_author:
            last_name = first_author.split(",")[0].strip()
        else:
            parts = first_author.split()
            last_name = parts[-1] if parts else "unknown"

        # Clean and convert to snake_case
        last_name = re.sub(r"[^a-zA-Z]", "", last_name).lower()
        return last_name or "unknown"

    def _extract_short_title(self, title: str, max_words: int = 3) -> str:
        """Extract short title for citation key."""
        # Remove special characters
        title = re.sub(r"[^\w\s]", "", title)

        # Split into words
        words = title.split()

        # Remove common stop words
        stop_words = {"the", "a", "an", "of", "for", "and", "or", "in", "on", "at", "to", "from"}
        meaningful_words = [w for w in words if w.lower() not in stop_words]

        # Take first N meaningful words
        short_words = meaningful_words[:max_words]

        # Convert to snake_case
        short_title = "_".join(w.lower() for w in short_words)

        return short_title or "untitled"

    # ══════════════════════════════════════════════════════════════════════
    # Formatting Helpers
    # ══════════════════════════════════════════════════════════════════════

    def _format_authors(self, authors: List[str]) -> str:
        """Format author list for BibTeX."""
        if not authors:
            return "Anonymous"

        # IEEE style: Last, First and Last, First
        return " and ".join(authors[:10])  # Limit to 10 authors

    def _clean_title(self, title: str) -> str:
        """Clean title for BibTeX entry."""
        # Remove extra whitespace
        title = re.sub(r"\s+", " ", title).strip()

        # Escape LaTeX special characters
        title = title.replace("{", "\\{").replace("}", "\\}")

        return title

    # ══════════════════════════════════════════════════════════════════════
    # Bibliography File Generation
    # ══════════════════════════════════════════════════════════════════════

    def format_bibliography(self, entries: List[Dict[str, str]]) -> str:
        """
        Format BibTeX entries into a complete bibliography file.

        Args:
            entries: List of entry dictionaries

        Returns:
            Formatted BibTeX file content
        """
        header = """% ═══════════════════════════════════════════════════════════════════════════
% Enhanced Bibliography - Auto-Generated
% ═══════════════════════════════════════════════════════════════════════════
%
% This file contains IEEE-formatted citations extracted from academic databases.
% Generated by: .dev_tools/research/bibtex_generator.py
% Format: IEEE
%
% Key Convention: topic_authorYear_shortTitle
%   Examples:
%     - smc_slotine1991_applied_nonlinear_control
%     - pso_kennedy1995_particle_swarm
%     - dip_khalil2002_nonlinear_systems
%
% ═══════════════════════════════════════════════════════════════════════════

"""

        # Sort entries by key
        entries_sorted = sorted(entries, key=lambda e: e["key"])

        # Format entries
        bibtex_entries = [e["entry"] for e in entries_sorted]

        return header + "\n\n".join(bibtex_entries) + "\n"

    def save_bibliography(
        self, entries: List[Dict[str, str]], output_path: Path
    ) -> None:
        """
        Save BibTeX entries to file.

        Args:
            entries: List of entry dictionaries
            output_path: Path to output .bib file
        """
        bibtex_text = self.format_bibliography(entries)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(bibtex_text)

        logger.info(f"Saved {len(entries)} entries to {output_path}")

    # ══════════════════════════════════════════════════════════════════════
    # Deduplication with Existing References
    # ══════════════════════════════════════════════════════════════════════

    def load_existing_keys(self, bib_file: Path) -> Set[str]:
        """
        Load existing citation keys from .bib file.

        Args:
            bib_file: Path to existing bibliography

        Returns:
            Set of citation keys
        """
        if not bib_file.exists():
            return set()

        with open(bib_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract citation keys
        pattern = r"@\w+\{([^,]+),"
        keys = set(re.findall(pattern, content))

        logger.info(f"Loaded {len(keys)} existing keys from {bib_file}")
        return keys

    def merge_with_existing(
        self, new_entries: List[Dict[str, str]], existing_file: Path
    ) -> List[Dict[str, str]]:
        """
        Merge new entries with existing bibliography, avoiding duplicates.

        Args:
            new_entries: New BibTeX entries
            existing_file: Path to existing .bib file

        Returns:
            Merged list of entries
        """
        existing_keys = self.load_existing_keys(existing_file)

        # Filter out duplicates
        unique_entries = [e for e in new_entries if e["key"] not in existing_keys]

        logger.info(
            f"Merged: {len(new_entries)} new → {len(unique_entries)} unique "
            f"({len(new_entries) - len(unique_entries)} duplicates removed)"
        )

        return unique_entries


# ═══════════════════════════════════════════════════════════════════════════
# Example Usage
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """Test BibTeX generator."""
    logging.basicConfig(level=logging.INFO)

    # Create sample papers
    papers = [
        Paper(
            title="Applied Nonlinear Control",
            authors=["Jean-Jacques E. Slotine", "Weiping Li"],
            year=1991,
            doi=None,
            url=None,
            abstract="Comprehensive treatment of nonlinear control",
            venue="Prentice Hall",
        ),
        Paper(
            title="Particle Swarm Optimization",
            authors=["James Kennedy", "Russell Eberhart"],
            year=1995,
            doi="10.1109/ICNN.1995.488968",
            url=None,
            abstract="Novel optimization algorithm based on swarm intelligence",
            venue="IEEE International Conference on Neural Networks",
        ),
    ]

    # Generate BibTeX
    gen = BibTeXGenerator()
    entries = gen.generate_entries(papers, topic="smc")

    # Print entries
    print("\nGenerated BibTeX Entries:\n")
    print(gen.format_bibliography(entries))


if __name__ == "__main__":
    main()
