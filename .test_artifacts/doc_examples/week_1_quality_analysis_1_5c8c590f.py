# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 1
# Runnable: True
# Hash: 5c8c590f

def extract_docstring(self, tree: ast.Module) -> Optional[str]:
    """Extract module docstring from AST."""
    docstring = ast.get_docstring(tree)
    if docstring:
        return self._clean_docstring(docstring)
    return None