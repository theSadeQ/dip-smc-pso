# Example from: docs\tools\claim_extraction_guide.md
# Index: 17
# Runnable: False
# Hash: 4d283e33

CITATION_PATTERNS = {
    # Existing patterns...
    'rfc': re.compile(r'RFC\s+(\d{4})', re.IGNORECASE),  # New: RFC citations
}