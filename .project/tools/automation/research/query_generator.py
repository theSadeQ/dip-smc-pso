# ═══════════════════════════════════════════════════════════════════════════
#  .dev_tools/research/query_generator.py
# ═══════════════════════════════════════════════════════════════════════════
"""
Query generation for academic research.

Converts technical claims into effective search queries for academic databases.
Extracts key technical terms, authors, and topics to maximize research relevance.

Strategy:
1. Extract mathematical/technical terms
2. Identify algorithm names and acronyms
3. Remove implementation-specific details
4. Generate multiple query variations
"""

import re
from typing import List
from dataclasses import dataclass


@dataclass
class Query:
    """Generated search query with metadata."""

    text: str
    priority: int  # 1 (highest) to 3 (lowest)
    keywords: List[str]
    query_type: str  # 'exact', 'broad', 'author', 'topic'


class QueryGenerator:
    """
    Generate academic search queries from technical claims.

    Examples:
        >>> gen = QueryGenerator()
        >>> queries = gen.generate("Implements super-twisting algorithm from Levant (2003)")
        >>> queries[0].text
        'super-twisting algorithm Levant'
    """

    # ══════════════════════════════════════════════════════════════════════
    # Technical Term Dictionaries
    # ══════════════════════════════════════════════════════════════════════

    ALGORITHM_PATTERNS = {
        # Sliding Mode Control variants
        r"super[\s-]?twisting": "super-twisting algorithm",
        r"\bsta\b": "super-twisting algorithm",
        r"classical\s+smc": "classical sliding mode control",
        r"adaptive\s+smc": "adaptive sliding mode control",
        r"sliding\s+mode": "sliding mode control",
        r"sliding\s+surface": "sliding mode control",  # Formal theorems use "sliding surface"
        r"\bsmc\b": "sliding mode control",
        r"boundary\s+layer\s+method": "sliding mode boundary layer",
        r"reaching\s+law": "sliding mode reaching law",
        r"reaching\s+condition": "sliding mode reaching condition",
        # PSO variants
        r"\bpso\b": "particle swarm optimization",
        r"particle\s+swarm": "particle swarm optimization",
        # Control theory
        r"lyapunov": "Lyapunov stability",
        r"mpc\b": "model predictive control",
        r"pid\b": "PID control",
        # Numerical methods
        r"runge[\s-]?kutta": "Runge-Kutta",
        r"\brk4\b": "Runge-Kutta",
    }

    MATHEMATICAL_TERMS = {
        "convergence",
        "stability",
        "asymptotic",
        "finite-time",
        "chattering",
        "boundary layer",
        "boundary layer method",
        "sliding surface",
        "reaching law",
        "reaching condition",
        "switching function",
        "switching gain",
        "control law",
        "gain",
        "theorem",
        "lemma",
        "proof",
        "Lyapunov",
        "matrix",
        "eigenvalue",
        "nonlinear",
        "linear",
        "exponentially stable",
        "ultimately bounded",
        "tracking error",
    }

    CONTROL_TOPICS = {
        "inverted pendulum",
        "double inverted pendulum",
        "DIP",
        "underactuated system",
        "stabilization",
        "tracking",
        "regulation",
        "robustness",
        "disturbance rejection",
        "fault detection",
        "FDI",
        "residual generation",
    }

    STOP_WORDS = {
        "implements",
        "implementation",
        "following",
        "based on",
        "according to",
        "from",
        "using",
        "with",
        "the",
        "this",
        "that",
        "these",
        "those",
        "here",
        "example",
        "e.g.",
        "i.e.",
        "etc",
        "code",
        "function",
        "class",
        "method",
        "module",
        "file",
        "script",
        "program",
    }

    # ══════════════════════════════════════════════════════════════════════
    # Query Generation Methods
    # ══════════════════════════════════════════════════════════════════════

    def generate(self, claim_text: str, max_queries: int = 5) -> List[Query]:
        """
        Generate multiple search queries from a claim.

        Args:
            claim_text: Technical claim text
            max_queries: Maximum number of query variations

        Returns:
            List of Query objects, sorted by priority
        """
        queries = []

        # Extract components
        authors = self._extract_authors(claim_text)
        algorithms = self._extract_algorithms(claim_text)
        math_terms = self._extract_mathematical_terms(claim_text)
        topics = self._extract_topics(claim_text)

        # Priority 1: Algorithm + Author (most specific)
        if algorithms and authors:
            for algo in algorithms[:2]:  # Top 2 algorithms
                for author in authors[:2]:  # Top 2 authors
                    queries.append(
                        Query(
                            text=f"{algo} {author}",
                            priority=1,
                            keywords=[algo, author],
                            query_type="exact",
                        )
                    )

        # Priority 2: Algorithm + Key Term (multiple variations)
        if algorithms:
            for algo in algorithms[:2]:
                if math_terms:
                    # Generate multiple algorithm+term combinations
                    for term in math_terms[:3]:  # Use top 3 math terms
                        queries.append(
                            Query(
                                text=f"{algo} {term}",
                                priority=2,
                                keywords=[algo, term],
                                query_type="broad",
                            )
                        )
                else:
                    queries.append(
                        Query(
                            text=algo,
                            priority=2,
                            keywords=[algo],
                            query_type="topic",
                        )
                    )

        # Priority 3: Topic + Mathematical Term (broadest)
        if topics and math_terms:
            topic = topics[0]
            term = math_terms[0]
            queries.append(
                Query(
                    text=f"{topic} {term}",
                    priority=3,
                    keywords=[topic, term],
                    query_type="broad",
                )
            )

        # Fallback 1: Generate mathematical concept pairs if we have < 3 queries
        if len(queries) < 3 and math_terms and len(math_terms) >= 2:
            # Create queries from pairs of mathematical terms
            for i, term1 in enumerate(math_terms[:3]):
                for term2 in math_terms[i+1:min(i+3, len(math_terms))]:
                    if len(queries) >= max_queries:
                        break
                    queries.append(
                        Query(
                            text=f"{term1} {term2}",
                            priority=3,
                            keywords=[term1, term2],
                            query_type="concept",
                        )
                    )
                if len(queries) >= max_queries:
                    break

        # Fallback 2: Single mathematical terms if still < 3 queries
        if len(queries) < 3 and math_terms:
            for term in math_terms[:max_queries - len(queries)]:
                queries.append(
                    Query(
                        text=term,
                        priority=3,
                        keywords=[term],
                        query_type="concept",
                    )
                )

        # Fallback 3: Clean claim text if no structured queries
        if not queries:
            cleaned = self._clean_text(claim_text)
            queries.append(
                Query(
                    text=cleaned,
                    priority=3,
                    keywords=[cleaned],
                    query_type="broad",
                )
            )

        # Sort by priority and limit
        queries.sort(key=lambda q: q.priority)
        return queries[:max_queries]

    def _extract_authors(self, text: str) -> List[str]:
        """
        Extract author names from claim text.

        Examples:
            "from Levant (2003)" → ["Levant"]
            "Slotine and Li (1991)" → ["Slotine", "Li"]
        """
        authors = []

        # Pattern: "Name (Year)"
        pattern = r"\b([A-Z][a-z]+(?:\s+(?:and|&)\s+[A-Z][a-z]+)?)\s*\((?:19|20)\d{2}\)"
        matches = re.findall(pattern, text)
        for match in matches:
            # Split "Name and Name" into separate authors
            names = re.split(r"\s+(?:and|&)\s+", match)
            authors.extend(names)

        # Pattern: "Name et al."
        pattern = r"\b([A-Z][a-z]+)\s+et\s+al\."
        matches = re.findall(pattern, text)
        authors.extend(matches)

        return list(dict.fromkeys(authors))  # Remove duplicates, preserve order

    def _extract_algorithms(self, text: str) -> List[str]:
        """Extract algorithm names and acronyms."""
        algorithms = []

        text_lower = text.lower()
        for pattern, canonical_name in self.ALGORITHM_PATTERNS.items():
            if re.search(pattern, text_lower):
                algorithms.append(canonical_name)

        return list(dict.fromkeys(algorithms))  # Remove duplicates

    def _extract_mathematical_terms(self, text: str) -> List[str]:
        """Extract mathematical and control theory terms."""
        text_lower = text.lower()
        found_terms = []

        for term in self.MATHEMATICAL_TERMS:
            if term.lower() in text_lower:
                found_terms.append(term)

        return found_terms

    def _extract_topics(self, text: str) -> List[str]:
        """Extract control system topics."""
        text_lower = text.lower()
        found_topics = []

        for topic in self.CONTROL_TOPICS:
            if topic.lower() in text_lower:
                found_topics.append(topic)

        return found_topics

    def _clean_text(self, text: str) -> str:
        """
        Clean claim text for direct search.

        Removes:
        - LaTeX math mode and symbols
        - MyST Markdown equation references
        - Common stop words
        - Implementation-specific terms
        - URLs and file paths
        - Special characters
        """
        # Remove LaTeX math mode ($...$)
        text = re.sub(r'\$[^$]+\$', '', text)

        # Remove MyST Markdown equation references ({eq}`...`)
        text = re.sub(r'\{eq\}`[^`]+`', '', text)

        # Remove LaTeX inline math escapes
        text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)

        # Remove comparison operators that lost context
        text = re.sub(r'\s+[<>]=?\s+', ' ', text)

        # Remove URLs
        text = re.sub(r"https?://\S+", "", text)

        # Remove file paths
        text = re.sub(r"[\w/\\]+\.py", "", text)

        # Remove common code patterns
        text = re.sub(r"[A-Z][a-z]+\(\)", "", text)  # ClassName()

        # Remove stop words
        words = text.split()
        filtered_words = [
            word
            for word in words
            if word.lower() not in self.STOP_WORDS and len(word) > 2
        ]

        # Join and clean
        cleaned = " ".join(filtered_words)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned[:200]  # Limit query length

    def generate_alternative_queries(
        self, claim_text: str, existing_results: int = 0
    ) -> List[Query]:
        """
        Generate alternative queries if initial search yielded few results.

        Strategy:
        - Broaden search terms
        - Use synonyms
        - Remove specificity

        Args:
            claim_text: Original claim text
            existing_results: Number of results from initial search

        Returns:
            List of alternative queries
        """
        alternatives = []

        if existing_results < 3:
            # Very broad: just algorithm name
            algorithms = self._extract_algorithms(claim_text)
            if algorithms:
                alternatives.append(
                    Query(
                        text=algorithms[0],
                        priority=3,
                        keywords=[algorithms[0]],
                        query_type="broad",
                    )
                )

            # Very broad: just topic
            topics = self._extract_topics(claim_text)
            if topics:
                alternatives.append(
                    Query(
                        text=topics[0],
                        priority=3,
                        keywords=[topics[0]],
                        query_type="topic",
                    )
                )

        return alternatives


# ═══════════════════════════════════════════════════════════════════════════
# Example Usage & Testing
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """Test query generator with sample claims."""
    gen = QueryGenerator()

    test_claims = [
        "Implements super-twisting algorithm from Levant (2003)",
        "Classical sliding mode control following Slotine and Li (1991)",
        "PSO optimization for controller gain tuning",
        "Lyapunov stability analysis for nonlinear systems",
        "Adaptive gain scheduling based on sliding surface magnitude",
    ]

    for claim in test_claims:
        print(f"\nClaim: {claim}")
        print("=" * 70)

        queries = gen.generate(claim, max_queries=3)
        for i, query in enumerate(queries, 1):
            print(
                f"{i}. [{query.priority}] {query.text:40s} ({query.query_type})"
            )
            print(f"   Keywords: {', '.join(query.keywords)}")

        print()


if __name__ == "__main__":
    main()
