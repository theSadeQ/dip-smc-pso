# Example from: docs\plans\citation_system\02_phase1_claim_extraction.md
# Index: 7
# Runnable: True
# Hash: 81bf3854

import ast

class CodeClaimExtractor(ast.NodeVisitor):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.claims = []
        self.current_scope = []  # Stack: ["module", "class:ClassName", "function:method"]

    def visit_Module(self, node: ast.Module):
        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_from_docstring(docstring, "module", 1)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.current_scope.append(f"class:{node.name}")
        docstring = ast.get_docstring(node)
        if docstring:
            scope = ':'.join(self.current_scope)
            self._extract_from_docstring(docstring, scope, node.lineno)
        self.generic_visit(node)
        self.current_scope.pop()

    def _extract_from_docstring(self, docstring: str, scope: str, line: int):
        # Pattern matching for implementation claims
        for match in self.PATTERNS['implements'].finditer(docstring):
            claim = CodeClaim(
                id=f"CODE-IMPL-{len(self.claims)+1:03d}",
                algorithm_name=match.group('what').strip(),
                source_attribution=match.group('source').strip(),
                scope=scope,
                file_path=str(self.file_path),
                line_number=line,
                has_citation=self._has_proper_citation(docstring),
                confidence=0.8
            )
            self.claims.append(claim)