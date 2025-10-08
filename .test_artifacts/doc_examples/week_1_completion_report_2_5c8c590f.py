# Example from: docs\plans\documentation\week_1_completion_report.md
# Index: 2
# Runnable: True
# Hash: 5c8c590f

def extract_docstring(self, tree: ast.Module) -> Optional[str]:
    """Extract module docstring from AST."""
    docstring = ast.get_docstring(tree)
    if docstring:
        return self._clean_docstring(docstring)
    return None