# Example from: docs\tools\claim_extraction_guide.md
# Index: 13
# Runnable: True
# Hash: 7bc42e5b

# Normalize whitespace before pattern matching
docstring_normalized = re.sub(r'\s+', ' ', docstring)
matches = THEOREM_PATTERN.finditer(docstring_normalized)