# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 8
# Runnable: False
# Hash: a1651c80

# example-metadata:
# runnable: false

PATTERNS = {
    'implements': re.compile(
        r'(?:Implements?|Implementation of|Based on)\s+'
        r'(?P<what>[^,\.]+?)\s+'
        r'(?:from|in|by)\s+'
        r'(?P<source>[^\.\n]+)',
        re.IGNORECASE
    ),
    'numbered_cite': re.compile(r'\[(\d+)\]'),
    'doi': re.compile(r'(?:doi:|https://doi\.org/)([^\s]+)', re.IGNORECASE),
    'author_year': re.compile(r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?)\s+(\d{4})\)')
}