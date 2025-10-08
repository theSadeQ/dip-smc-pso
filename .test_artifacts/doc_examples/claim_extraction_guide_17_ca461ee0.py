# Example from: docs\tools\claim_extraction_guide.md
# Index: 17
# Runnable: False
# Hash: ca461ee0

# example-metadata:
# runnable: false

CITATION_PATTERNS = {
    # Existing patterns...
    'rfc': re.compile(r'RFC\s+(\d{4})', re.IGNORECASE),  # New: RFC citations
}