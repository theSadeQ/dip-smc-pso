# Example from: docs\tools\claim_extraction_guide.md
# Index: 9
# Runnable: True
# Hash: 123cfbac

# In formal_extractor.py, modify pattern:
THEOREM_PATTERN = re.compile(
    r'(?<!Example[:\s])(?<!e\.g\.[:\s])'  # Negative lookbehind
    r'\*\*Theorem\s+(\d+\.?\d*)\*\*'
)