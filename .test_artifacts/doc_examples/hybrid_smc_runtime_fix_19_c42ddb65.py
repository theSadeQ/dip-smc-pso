# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 19
# Runnable: True
# Hash: c42ddb65

# scripts/code_review_automation.py
import ast
import argparse
from typing import List, Tuple

class ControllerCodeReviewer:
    """Automated code review for controller methods."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.tree = ast.parse(f.read())

    def check_return_statements(self) -> List[str]:
        """Check for missing return statements in typed methods."""
        issues = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.returns:
                if not self._has_return_statement(node):
                    issues.append(
                        f"Method '{node.name}' (line {node.lineno}) "
                        f"has return type annotation but no return statement"
                    )

        return issues

    def check_variable_scope_in_returns(self) -> List[str]:
        """Check for out-of-scope variables in return statements."""
        issues = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                local_vars = self._get_local_variables(node)

                for child in ast.walk(node):
                    if isinstance(child, ast.Return) and child.value:
                        used_vars = self._get_used_variables(child.value)
                        out_of_scope = used_vars - local_vars - {'self'}

                        if out_of_scope:
                            issues.append(
                                f"Method '{node.name}' return statement uses "
                                f"out-of-scope variables: {out_of_scope}"
                            )

        return issues

    def _has_return_statement(self, func_node: ast.FunctionDef) -> bool:
        """Check if function has explicit return statement."""
        for child in ast.walk(func_node):
            if isinstance(child, ast.Return):
                return True
        return False

    def _get_local_variables(self, func_node: ast.FunctionDef) -> set:
        """Extract local variable names from function."""
        local_vars = set()

        # Add parameters
        for arg in func_node.args.args:
            local_vars.add(arg.arg)

        # Add assigned variables
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        local_vars.add(target.id)

        return local_vars

    def _get_used_variables(self, node: ast.AST) -> set:
        """Extract variable names used in AST node."""
        used_vars = set()

        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                used_vars.add(child.id)

        return used_vars

def main():
    parser = argparse.ArgumentParser(description='Review controller code')
    parser.add_argument('file', help='Python file to review')
    args = parser.parse_args()

    reviewer = ControllerCodeReviewer(args.file)

    issues = []
    issues.extend(reviewer.check_return_statements())
    issues.extend(reviewer.check_variable_scope_in_returns())

    if issues:
        print("Code Review Issues Found:")
        for issue in issues:
            print(f"  ❌ {issue}")
        exit(1)
    else:
        print("✅ Code review passed - no issues found")

if __name__ == "__main__":
    main()