# Example from: docs\tools\ast_traversal_patterns.md
# Index: 7
# Runnable: True
# Hash: 2add58d1

def batch_extract(file_paths: List[str]) -> List[Dict]:
    claims = []
    for path in file_paths:
        tree = ast.parse(Path(path).read_text())  # O(n)
        extractor = CodeClaimExtractor()           # O(1)
        extractor.visit(tree)                      # O(m)
        claims.extend(extractor.claims)            # O(c)
        # Tree garbage collected here, amortized O(1) per file
    return claims