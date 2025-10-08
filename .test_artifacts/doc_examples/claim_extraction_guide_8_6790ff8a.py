# Example from: docs\tools\claim_extraction_guide.md
# Index: 8
# Runnable: True
# Hash: 6790ff8a

# Skip files with no docstrings
if not any(hasattr(node, 'body') for node in ast.walk(tree)):
    return []  # No docstrings possible