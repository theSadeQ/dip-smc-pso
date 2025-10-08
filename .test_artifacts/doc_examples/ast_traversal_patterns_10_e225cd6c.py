# Example from: docs\tools\ast_traversal_patterns.md
# Index: 10
# Runnable: True
# Hash: e225cd6c

def single_quotes():
    'Single-line with citation [1]'  # ✅ Detected

def triple_single():
    '''Triple single quotes
    spanning multiple lines'''  # ✅ Detected