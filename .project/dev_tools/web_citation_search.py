#!/usr/bin/env python3
#======================================================================================\\\
#======================= .dev_tools/web_citation_search.py ============================\\\
#======================================================================================\\\

"""
Web-Based Citation Discovery for DIP-SMC-PSO Project.

This module provides Tier 2 citation discovery using web search when
algorithms/concepts are not found in the canonical database.

Features:
- Targeted web searches for academic papers and textbooks
- DOI extraction and validation
- ISBN extraction for textbooks
- Confidence scoring based on result quality
- Multiple fallback strategies
"""

from typing import Dict, Optional, List, Tuple
import re
import json


def search_algorithm_citation(algorithm_name: str, code_context: str = "") -> Optional[Dict]:
    """
    Search for algorithm citation using web search.

    Args:
        algorithm_name: Name of the algorithm to search for
        code_context: Additional context from code (helps refine search)

    Returns:
        Citation dict if found with high confidence, None otherwise
    """
    # Build targeted search query
    query = build_algorithm_search_query(algorithm_name, code_context)

    # Perform web search (using WebSearch tool)
    print(f"  [Web Search] Query: {query}")

    # NOTE: This is a placeholder for actual WebSearch integration
    # In the actual implementation, we would use:
    # from claude_tools import WebSearch
    # results = WebSearch(query=query)

    # For now, return None (will be implemented in main engine with actual WebSearch tool)
    return None


def search_concept_citation(concept: str, domain: str = "control theory") -> Optional[Dict]:
    """
    Search for concept citation in textbooks using web search.

    Args:
        concept: Control theory concept to search for
        domain: Domain context (e.g., "control theory", "optimization")

    Returns:
        Citation dict if found with high confidence, None otherwise
    """
    # Build targeted search query
    query = build_concept_search_query(concept, domain)

    print(f"  [Web Search] Query: {query}")

    # Placeholder for actual WebSearch integration
    return None


def build_algorithm_search_query(algorithm_name: str, context: str = "") -> str:
    """
    Build optimized search query for finding algorithm papers.

    Args:
        algorithm_name: Algorithm name
        context: Additional context

    Returns:
        Optimized search query string
    """
    # Base query
    query_parts = [algorithm_name, "original paper", "DOI"]

    # Add context hints if available
    if "optimization" in context.lower():
        query_parts.append("optimization")
    elif "control" in context.lower():
        query_parts.append("control")
    elif "numerical" in context.lower() or "integration" in context.lower():
        query_parts.append("numerical methods")

    # Add common author names for well-known algorithms
    author_hints = {
        "differential evolution": "Storn Price",
        "particle swarm": "Kennedy Eberhart",
        "kalman": "Kalman",
        "super-twisting": "Levant",
        "sliding mode": "Utkin",
        "backstepping": "Krstic",
        "nelder-mead": "Nelder Mead"
    }

    for key, authors in author_hints.items():
        if key in algorithm_name.lower():
            query_parts.append(authors)
            break

    return " ".join(query_parts)


def build_concept_search_query(concept: str, domain: str) -> str:
    """
    Build optimized search query for finding textbook references.

    Args:
        concept: Concept name
        domain: Domain context

    Returns:
        Optimized search query string
    """
    query_parts = [concept, domain, "textbook", "ISBN"]

    # Add well-known textbook authors
    if "lyapunov" in concept.lower() or "nonlinear" in concept.lower():
        query_parts.append("Khalil")
    elif "overshoot" in concept.lower() or "settling time" in concept.lower():
        query_parts.append("Ogata")
    elif "mpc" in concept.lower() or "predictive" in concept.lower():
        query_parts.append("Camacho")
    elif "sliding mode" in concept.lower():
        query_parts.append("Utkin")

    return " ".join(query_parts)


def extract_doi_from_text(text: str) -> Optional[str]:
    """
    Extract DOI from text using regex patterns.

    Args:
        text: Text to search for DOI

    Returns:
        DOI string if found, None otherwise
    """
    # DOI patterns
    patterns = [
        r'10\.\d{4,}/[^\s]+',  # Standard DOI format
        r'doi:\s*10\.\d{4,}/[^\s]+',  # With 'doi:' prefix
        r'https://doi\.org/10\.\d{4,}/[^\s]+'  # Full DOI URL
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            doi = match.group(0)
            # Clean up
            doi = doi.replace('doi:', '').replace('https://doi.org/', '').strip()
            return doi

    return None


def extract_isbn_from_text(text: str) -> Optional[str]:
    """
    Extract ISBN from text using regex patterns.

    Args:
        text: Text to search for ISBN

    Returns:
        ISBN string if found, None otherwise
    """
    # ISBN patterns (ISBN-10 and ISBN-13)
    patterns = [
        r'ISBN[-‐]?13?:?\s*(97[89][-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?\d)',  # ISBN-13
        r'ISBN[-‐]?10?:?\s*(\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dX])',  # ISBN-10
        r'(97[89]\d{10})',  # Raw ISBN-13
        r'(\d{9}[\dX])'  # Raw ISBN-10
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            isbn = match.group(1) if match.lastindex else match.group(0)
            # Normalize: remove hyphens and spaces
            isbn = re.sub(r'[-\s]', '', isbn)
            # Validate length
            if len(isbn) in [10, 13]:
                return isbn

    return None


def extract_paper_title_from_text(text: str, algorithm_name: str) -> Optional[str]:
    """
    Extract paper title from search results.

    Args:
        text: Search result text
        algorithm_name: Algorithm name to validate against

    Returns:
        Paper title if found and validated, None otherwise
    """
    # Look for common title patterns
    patterns = [
        r'"([^"]+)"',  # Quoted titles
        r'<title>([^<]+)</title>',  # HTML title tags
        r'Title:\s*([^\n]+)',  # Explicit "Title:" labels
    ]

    candidates = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        candidates.extend(matches)

    # Filter candidates: must mention algorithm name
    algorithm_lower = algorithm_name.lower()
    for candidate in candidates:
        if algorithm_lower in candidate.lower():
            # Clean up
            title = candidate.strip()
            title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
            if 10 < len(title) < 200:  # Reasonable title length
                return title

    return None


def extract_authors_from_text(text: str) -> Optional[str]:
    """
    Extract author names from search results.

    Args:
        text: Search result text

    Returns:
        Author string if found, None otherwise
    """
    # Look for common author patterns
    patterns = [
        r'Authors?:\s*([^\n]+)',
        r'By\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            authors = match.group(1).strip()
            # Basic validation
            if len(authors) < 100:  # Reasonable length
                return authors

    return None


def extract_year_from_text(text: str) -> Optional[int]:
    """
    Extract publication year from search results.

    Args:
        text: Search result text

    Returns:
        Year as integer if found, None otherwise
    """
    # Look for year patterns
    patterns = [
        r'(\d{4})',  # Four-digit number
        r'Year:\s*(\d{4})',
        r'\((\d{4})\)',  # Year in parentheses
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            year = int(match)
            # Validate reasonable year range
            if 1950 <= year <= 2025:
                return year

    return None


def validate_algorithm_paper_match(paper_title: str, algorithm_name: str) -> bool:
    """
    Validate that paper title matches algorithm name.

    Args:
        paper_title: Extracted paper title
        algorithm_name: Target algorithm name

    Returns:
        True if match is confident, False otherwise
    """
    if not paper_title or not algorithm_name:
        return False

    title_lower = paper_title.lower()
    algorithm_lower = algorithm_name.lower()

    # Direct match
    if algorithm_lower in title_lower:
        return True

    # Check word overlap
    algorithm_words = set(algorithm_lower.split())
    title_words = set(title_lower.split())

    overlap = algorithm_words.intersection(title_words)
    overlap_ratio = len(overlap) / len(algorithm_words) if algorithm_words else 0

    # Require at least 50% word overlap
    return overlap_ratio >= 0.5


def calculate_citation_confidence(citation: Dict, algorithm_name: str) -> float:
    """
    Calculate confidence score for discovered citation.

    Args:
        citation: Citation dict with extracted fields
        algorithm_name: Target algorithm name

    Returns:
        Confidence score (0.0 to 1.0)
    """
    score = 0.0

    # Has DOI/ISBN (20 points)
    if citation.get('doi_or_url') or citation.get('isbn'):
        score += 0.2

    # Has title (20 points)
    if citation.get('paper_title') or citation.get('book_title'):
        score += 0.2

    # Has authors (10 points)
    if citation.get('authors'):
        score += 0.1

    # Has year (10 points)
    if citation.get('year'):
        score += 0.1

    # Title matches algorithm (40 points)
    title = citation.get('paper_title') or citation.get('book_title') or ''
    if validate_algorithm_paper_match(title, algorithm_name):
        score += 0.4

    return min(score, 1.0)


def format_citation_for_csv(citation: Dict, category: str) -> Dict:
    """
    Format discovered citation for CSV export.

    Args:
        citation: Raw citation data
        category: Category (A or B)

    Returns:
        Formatted citation dict matching CSV schema
    """
    if category == "A":
        # Algorithm paper
        return {
            "algorithm_name": citation.get("algorithm_name", ""),
            "suggested_citation": citation.get("suggested_citation", ""),
            "bibtex_key": citation.get("bibtex_key", ""),
            "doi_or_url": citation.get("doi_or_url", ""),
            "paper_title": citation.get("paper_title", ""),
            "authors": citation.get("authors", ""),
            "year": citation.get("year", ""),
            "reference_type": citation.get("reference_type", "journal"),
            "verification": citation.get("verification", "Web search discovery")
        }
    else:  # Category B
        # Textbook concept
        return {
            "concept": citation.get("concept", ""),
            "suggested_citation": citation.get("suggested_citation", ""),
            "bibtex_key": citation.get("bibtex_key", ""),
            "isbn": citation.get("isbn", ""),
            "book_title": citation.get("book_title", ""),
            "authors": citation.get("authors", ""),
            "year": citation.get("year", ""),
            "reference_type": "book",
            "chapter_section": citation.get("chapter_section", "")
        }


# ===========================================================================================
# WEB SEARCH RESULT PARSING
# ===========================================================================================

def parse_web_search_results(results: str, algorithm_name: str, category: str) -> Optional[Dict]:
    """
    Parse web search results to extract citation information.

    This function would be called with actual WebSearch results.
    For now, it returns None (integrated in main engine).

    Args:
        results: Raw web search results (text)
        algorithm_name: Target algorithm name
        category: Category A or B

    Returns:
        Parsed citation dict if successful, None otherwise
    """
    # Extract key components
    doi = extract_doi_from_text(results)
    isbn = extract_isbn_from_text(results)
    title = extract_paper_title_from_text(results, algorithm_name)
    authors = extract_authors_from_text(results)
    year = extract_year_from_text(results)

    # Validate minimum requirements
    if category == "A":
        # Papers need DOI and title
        if not doi or not title:
            return None
    else:  # Category B
        # Textbooks need ISBN and title
        if not isbn or not title:
            return None

    # Build citation dict
    if category == "A":
        citation = {
            "algorithm_name": algorithm_name,
            "doi_or_url": doi,
            "paper_title": title,
            "authors": authors or "Unknown",
            "year": year or 2000,
            "reference_type": "journal",
            "verification": "Discovered via web search"
        }
    else:
        citation = {
            "concept": algorithm_name,
            "isbn": isbn,
            "book_title": title,
            "authors": authors or "Unknown",
            "year": year or 2000,
            "reference_type": "book",
            "chapter_section": ""
        }

    # Calculate confidence
    confidence = calculate_citation_confidence(citation, algorithm_name)

    # Only return if confidence is high enough
    if confidence >= 0.6:
        citation['confidence_score'] = confidence
        return citation

    return None


# ===========================================================================================
# CITATION SUGGESTIONS BASED ON KEYWORDS
# ===========================================================================================

def suggest_citation_from_keywords(text: str, category: str) -> Optional[str]:
    """
    Suggest a likely citation based on keywords in text.

    This is a fallback heuristic when web search fails.

    Args:
        text: Code summary or rationale
        category: Category A or B

    Returns:
        Suggested citation key, or None
    """
    text_lower = text.lower()

    # Keyword-based suggestions for Category A
    if category == "A":
        if any(kw in text_lower for kw in ["runge-kutta", "rk4", "rk45"]):
            return "hairer1993solving"
        if any(kw in text_lower for kw in ["particle swarm", "pso"]):
            return "kennedy1995particle"
        if any(kw in text_lower for kw in ["differential evolution", "de/rand"]):
            return "storn1997differential"
        if "kalman" in text_lower:
            return "kalman1960new"
        if any(kw in text_lower for kw in ["super-twisting", "super twisting"]):
            return "levant1993sliding"
        if any(kw in text_lower for kw in ["sliding mode", "smc"]):
            return "utkin1977variable"

    # Keyword-based suggestions for Category B
    elif category == "B":
        if any(kw in text_lower for kw in ["overshoot", "settling time", "rise time"]):
            return "ogata2010modern"
        if "lyapunov" in text_lower:
            return "khalil2002nonlinear"
        if any(kw in text_lower for kw in ["mpc", "model predictive"]):
            return "camacho2013model"
        if "sliding surface" in text_lower or "chattering" in text_lower:
            return "utkin1992sliding"

    return None


# ===========================================================================================
# MAIN INTERFACE
# ===========================================================================================

def discover_citation_with_web(
    claim: Dict,
    use_web_search: bool = True
) -> Tuple[Optional[Dict], str]:
    """
    Main interface for web-based citation discovery.

    Args:
        claim: Claim dict with code_summary, rationale, category
        use_web_search: If False, only use keyword suggestions

    Returns:
        Tuple of (citation_dict, discovery_method)
        - citation_dict: Discovered citation or None
        - discovery_method: "web_search", "keyword_suggestion", or "not_found"
    """
    category = claim.get('category')
    code_summary = claim.get('code_summary', '')
    rationale = claim.get('rationale', '')

    # Extract algorithm/concept name
    if category == "A":
        # Try to extract algorithm name from code_summary
        algorithm_name = code_summary.split('algorithm')[0].strip() if 'algorithm' in code_summary else code_summary
    else:
        algorithm_name = code_summary

    # Web search (if enabled and available)
    if use_web_search:
        # NOTE: Actual web search would be integrated here
        # For now, we skip to keyword suggestions
        pass

    # Fallback to keyword suggestions
    suggested_key = suggest_citation_from_keywords(code_summary + " " + rationale, category)
    if suggested_key:
        # Import database to get full citation
        import citation_database as db
        if category == "A" and suggested_key in [c['bibtex_key'] for c in db.ALGORITHM_CITATIONS.values()]:
            for key, cit in db.ALGORITHM_CITATIONS.items():
                if cit['bibtex_key'] == suggested_key:
                    return cit, "keyword_suggestion"
        elif category == "B" and suggested_key in [c['bibtex_key'] for c in db.CONCEPT_CITATIONS.values()]:
            for key, cit in db.CONCEPT_CITATIONS.items():
                if cit['bibtex_key'] == suggested_key:
                    return cit, "keyword_suggestion"

    return None, "not_found"
