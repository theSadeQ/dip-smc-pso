"""
Analyze Python source files for missing API documentation.
Focuses on public APIs (classes, methods, functions) without proper docstrings.
"""

import ast
import json
import os
from pathlib import Path
from typing import List, Dict, Any


class APIDocAnalyzer(ast.NodeVisitor):
    """AST visitor to find undocumented public APIs."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.issues = []
        self.current_class = None

    def is_public(self, name: str) -> bool:
        """Check if name is public (not starting with _)."""
        return not name.startswith('_') or name.startswith('__') and name.endswith('__')

    def has_adequate_docstring(self, node) -> bool:
        """Check if node has a docstring."""
        return ast.get_docstring(node) is not None

    def visit_ClassDef(self, node):
        """Visit class definitions."""
        if self.is_public(node.name):
            if not self.has_adequate_docstring(node):
                self.issues.append({
                    "file": self.filepath,
                    "line": node.lineno,
                    "type": "class_docstring_missing",
                    "api_name": node.name,
                    "severity": "critical",
                    "impact": f"Public class '{node.name}' lacks docstring"
                })

        # Visit methods within class
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        """Visit function/method definitions."""
        if self.is_public(node.name):
            if not self.has_adequate_docstring(node):
                if self.current_class:
                    api_name = f"{self.current_class}.{node.name}"
                    issue_type = "method_docstring_missing"
                    impact = f"Public method '{api_name}' lacks docstring"
                else:
                    api_name = node.name
                    issue_type = "function_docstring_missing"
                    impact = f"Public function '{node.name}' lacks docstring"

                self.issues.append({
                    "file": self.filepath,
                    "line": node.lineno,
                    "type": issue_type,
                    "api_name": api_name,
                    "severity": "critical",
                    "impact": impact
                })
            else:
                # Check for parameter documentation
                docstring = ast.get_docstring(node)
                if docstring and node.args.args:
                    # Check if Parameters section exists
                    if "Parameters" not in docstring and "Args:" not in docstring:
                        if len(node.args.args) > 1 or (len(node.args.args) == 1 and node.args.args[0].arg != 'self'):
                            api_name = f"{self.current_class}.{node.name}" if self.current_class else node.name
                            self.issues.append({
                                "file": self.filepath,
                                "line": node.lineno,
                                "type": "parameter_docs_missing",
                                "api_name": api_name,
                                "severity": "high",
                                "impact": f"Function '{api_name}' has parameters but no parameter documentation"
                            })

                # Check for return type documentation
                if docstring and node.returns:
                    if "Returns" not in docstring and "return" not in docstring.lower():
                        api_name = f"{self.current_class}.{node.name}" if self.current_class else node.name
                        self.issues.append({
                            "file": self.filepath,
                            "line": node.lineno,
                            "type": "return_docs_missing",
                            "api_name": api_name,
                            "severity": "medium",
                            "impact": f"Function '{api_name}' has return type but no return documentation"
                        })

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function definitions."""
        self.visit_FunctionDef(node)


def analyze_file(filepath: Path) -> List[Dict[str, Any]]:
    """Analyze a single Python file for missing API documentation."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)
        analyzer = APIDocAnalyzer(str(filepath))
        analyzer.visit(tree)
        return analyzer.issues
    except SyntaxError:
        return []
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return []


def analyze_directory(base_path: Path, pattern: str = "**/*.py") -> List[Dict[str, Any]]:
    """Analyze all Python files in a directory."""
    all_issues = []

    for filepath in base_path.glob(pattern):
        # Skip test files and __pycache__
        if '__pycache__' in str(filepath) or 'test_' in filepath.name:
            continue

        issues = analyze_file(filepath)
        all_issues.extend(issues)

    return all_issues


def main():
    """Main analysis function."""
    base_path = Path(r"D:\Projects\main\src")

    # Analyze specific directories
    target_dirs = [
        "controllers",
        "core",
        "optimization",
        "plant",
        "utils",
        "simulation",
        "analysis",
        "interfaces"
    ]

    all_issues = []

    for dir_name in target_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"Analyzing {dir_name}...")
            issues = analyze_directory(dir_path)
            all_issues.extend(issues)
            print(f"  Found {len(issues)} issues")

    # Sort by severity and file
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    all_issues.sort(key=lambda x: (severity_order.get(x['severity'], 4), x['file'], x['line']))

    # Save results
    output_file = Path(r"D:\Projects\main\.test_artifacts\p0_api_docs_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"p0_missing_api_docs": all_issues}, f, indent=2)

    print(f"\nTotal issues found: {len(all_issues)}")
    print(f"Results saved to {output_file}")

    # Print summary by type
    by_type = {}
    for issue in all_issues:
        issue_type = issue['type']
        by_type[issue_type] = by_type.get(issue_type, 0) + 1

    print("\nBreakdown by type:")
    for issue_type, count in sorted(by_type.items()):
        print(f"  {issue_type}: {count}")


if __name__ == "__main__":
    main()
