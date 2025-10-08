# Example from: docs\plans\documentation\week_1_quality_analysis.md
# Index: 6
# Runnable: True
# Hash: e50415a3

def extract_docstring(self, tree: ast.Module) -> Optional[str]:
    """Extract module docstring from AST.

    Args:
        tree: Parsed AST tree

    Returns:
        Cleaned docstring or None if not found
    """