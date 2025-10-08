# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 14
# Runnable: True
# Hash: 391d72eb

# Pre-commit hook: validate_return_statements.py
import ast
import sys

def check_return_statements(file_path):
    """Verify all methods with return type annotations have return statements."""

    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.returns:  # Has return type annotation
                # Check if method body contains return statement
                has_return = any(
                    isinstance(child, ast.Return)
                    for child in ast.walk(node)
                )

                if not has_return:
                    print(f"ERROR: {node.name} missing return statement")
                    return False

    return True

if __name__ == "__main__":
    file_path = sys.argv[1]
    if not check_return_statements(file_path):
        sys.exit(1)