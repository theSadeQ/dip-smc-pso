# Example from: docs\tools\claim_extraction_guide.md
# Index: 12
# Runnable: True
# Hash: cf348e37

# Support "Thm" in addition to "Theorem"
THEOREM_PATTERN = re.compile(
    r'\*\*(Theorem|Thm\.?)\s+(\d+\.?\d*)\*\*'
)