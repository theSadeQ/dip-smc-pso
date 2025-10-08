# Example from: docs\tools\ast_traversal_patterns.md
# Index: 3
# Runnable: True
# Hash: 89c7e573

import ast
from typing import List, Dict

class CodeClaimExtractor(ast.NodeVisitor):
    def __init__(self):
        self.claims: List[Dict] = []
        self.scope_stack: List[str] = []  # Hierarchical scope tracker

    def visit_Module(self, node: ast.Module) -> None:
        """Process module-level docstring."""
        self.scope_stack.append("module")

        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_claims(docstring, scope=":".join(self.scope_stack))

        self.generic_visit(node)  # Continue to children
        self.scope_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Process class definition with correct scope."""
        self.scope_stack.append(f"class:{node.name}")

        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_claims(docstring, scope=":".join(self.scope_stack))

        self.generic_visit(node)  # Visit methods
        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Process function/method with nested scope support."""
        self.scope_stack.append(f"function:{node.name}")

        docstring = ast.get_docstring(node)
        if docstring:
            self._extract_claims(docstring, scope=":".join(self.scope_stack))

        self.generic_visit(node)  # Handle nested functions
        self.scope_stack.pop()

    def _extract_claims(self, docstring: str, scope: str) -> None:
        """Apply regex patterns to docstring with known scope."""
        # Now regex operates on clean docstring text with correct scope
        for pattern in CITATION_PATTERNS:
            for match in pattern.finditer(docstring):
                self.claims.append({
                    "text": match.group(0),
                    "scope": scope,  # ✅ Guaranteed correct
                    "line": match.start()
                })