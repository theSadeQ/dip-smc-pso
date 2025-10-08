# Example from: docs\tools\ast_traversal_patterns.md
# Index: 5
# Runnable: False
# Hash: 0dcb829d

def extract_all_citations(docstring: str) -> List[Dict]:
    citations = []

    for pattern_name, pattern in CITATION_PATTERNS.items():
        for match in pattern.finditer(docstring):
            citations.append({
                "type": pattern_name,
                "match": match.groupdict(),
                "start": match.start(),
                "end": match.end()
            })

    return citations