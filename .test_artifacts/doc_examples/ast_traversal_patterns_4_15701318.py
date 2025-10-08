# Example from: docs\tools\ast_traversal_patterns.md
# Index: 4
# Runnable: True
# Hash: 15701318

import re

CITATION_PATTERNS = {
    'implements': re.compile(
        r'(?:Implements?|Implementation of|Based on)\s+'
        r'(?P<what>[^,\.]+?)\s+'
        r'(?:from|in|by)\s+'
        r'(?P<source>[^\.\n]+)',
        re.IGNORECASE
    ),

    'numbered_cite': re.compile(
        r'\[(?P<ref>\d+)\]'
    ),

    'doi': re.compile(
        r'(?:doi|DOI):\s*(?P<doi>[^\s,]+)',
        re.IGNORECASE
    ),

    'author_year': re.compile(
        r'\((?P<author>[A-Z][a-z]+(?:\s+et al\.)?)\s+(?P<year>\d{4})\)'
    ),

    'arxiv': re.compile(
        r'arXiv:\s*(?P<id>\d{4}\.\d{4,5})',
        re.IGNORECASE
    )
}