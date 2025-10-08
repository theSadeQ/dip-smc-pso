# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 8
# Runnable: False
# Hash: 261d6cd3

# scripts/validate_return_statements.py
def validate_return_statements(file_path):
    """Ensure methods with return type annotations have return statements."""
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.returns:
            if not has_return_statement(node):
                raise ValueError(
                    f"Method '{node.name}' has return type annotation "
                    f"but missing return statement"
                )