# Example from: docs\tools\ast_traversal_patterns.md
# Index: 2
# Runnable: True
# Hash: 73d02323

REGEX_IMPLEMENTS = re.compile(
    r'(?:Implements?|Implementation of)\s+([^,\.]+?)\s+from\s+([^\.\n]+)',
    re.IGNORECASE | re.MULTILINE
)