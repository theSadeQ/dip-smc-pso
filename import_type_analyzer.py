#======================================================================================\\\
#============================== import_type_analyzer.py ===============================\\\
#======================================================================================\\\

"""Analyze and optimize import organization and type hint coverage."""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

class ImportAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze imports and type hints."""

    def __init__(self):
        self.imports = []
        self.from_imports = []
        self.functions = []
        self.classes = []
        self.type_hints = []
        self.missing_hints = []

    def visit_Import(self, node):
        for alias in node.aliases:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname,
                'line': node.lineno
            })

    def visit_ImportFrom(self, node):
        for alias in node.aliases:
            self.from_imports.append({
                'module': node.module,
                'name': alias.name,
                'alias': alias.asname,
                'line': node.lineno
            })

    def visit_FunctionDef(self, node):
        # Analyze function type hints
        has_return_hint = node.returns is not None
        param_hints = []
        missing_param_hints = []

        for arg in node.args.args:
            if arg.annotation:
                param_hints.append(arg.arg)
            else:
                missing_param_hints.append(arg.arg)

        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'has_return_hint': has_return_hint,
            'param_hints': param_hints,
            'missing_param_hints': missing_param_hints,
            'total_params': len(node.args.args),
            'hint_coverage': len(param_hints) / len(node.args.args) if node.args.args else 1.0
        })

        if not has_return_hint and node.name != '__init__':
            self.missing_hints.append({
                'type': 'return',
                'function': node.name,
                'line': node.lineno
            })

        for param in missing_param_hints:
            if param != 'self':  # Skip 'self' parameter
                self.missing_hints.append({
                    'type': 'parameter',
                    'function': node.name,
                    'parameter': param,
                    'line': node.lineno
                })

    def visit_AsyncFunctionDef(self, node):
        # Handle async functions same as regular functions
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.classes.append({
            'name': node.name,
            'line': node.lineno
        })

def analyze_file_imports_and_types(file_path: str) -> Dict[str, Any]:
    """Analyze imports and type hints in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)
        analyzer = ImportAnalyzer()
        analyzer.visit(tree)

        # Categorize imports
        stdlib_imports = []
        third_party_imports = []
        local_imports = []

        # Standard library modules (partial list)
        stdlib_modules = {
            'os', 'sys', 'json', 'pickle', 'typing', 'pathlib', 'argparse',
            'logging', 'datetime', 'collections', 'itertools', 'functools',
            'operator', 'abc', 'copy', 'random', 'time', 'math', 'statistics',
            're', 'string', 'io', 'warnings', 'unittest', 'tempfile'
        }

        for imp in analyzer.imports + analyzer.from_imports:
            module = imp.get('module') or imp.get('name', '')
            if not module:
                continue

            root_module = module.split('.')[0]
            if root_module in stdlib_modules:
                stdlib_imports.append(imp)
            elif module.startswith('src.') or module.startswith('.'):
                local_imports.append(imp)
            else:
                third_party_imports.append(imp)

        # Calculate type hint coverage
        total_functions = len(analyzer.functions)
        functions_with_return_hints = sum(1 for f in analyzer.functions if f['has_return_hint'])
        total_params = sum(f['total_params'] for f in analyzer.functions)
        params_with_hints = sum(len(f['param_hints']) for f in analyzer.functions)

        return {
            'file_path': file_path,
            'imports': {
                'stdlib': stdlib_imports,
                'third_party': third_party_imports,
                'local': local_imports,
                'total': len(analyzer.imports) + len(analyzer.from_imports)
            },
            'type_hints': {
                'functions': analyzer.functions,
                'missing_hints': analyzer.missing_hints,
                'total_functions': total_functions,
                'functions_with_return_hints': functions_with_return_hints,
                'return_hint_coverage': functions_with_return_hints / total_functions if total_functions > 0 else 1.0,
                'total_params': total_params,
                'params_with_hints': params_with_hints,
                'param_hint_coverage': params_with_hints / total_params if total_params > 0 else 1.0
            },
            'classes': analyzer.classes
        }

    except Exception as e:
        return {
            'file_path': file_path,
            'error': str(e),
            'imports': {'stdlib': [], 'third_party': [], 'local': [], 'total': 0},
            'type_hints': {
                'functions': [], 'missing_hints': [], 'total_functions': 0,
                'functions_with_return_hints': 0, 'return_hint_coverage': 0.0,
                'total_params': 0, 'params_with_hints': 0, 'param_hint_coverage': 0.0
            },
            'classes': []
        }

def check_import_organization(file_path: str) -> Dict[str, Any]:
    """Check if imports are properly organized."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        import_lines = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                import_lines.append((i + 1, stripped))

        if not import_lines:
            return {'organized': True, 'issues': []}

        # Check grouping (stdlib -> third-party -> local)
        issues = []
        current_group = 'stdlib'
        last_import_line = 0

        stdlib_modules = {
            'os', 'sys', 'json', 'pickle', 'typing', 'pathlib', 'argparse',
            'logging', 'datetime', 'collections', 'itertools', 'functools',
            'operator', 'abc', 'copy', 'random', 'time', 'math', 'statistics',
            're', 'string', 'io', 'warnings', 'unittest', 'tempfile'
        }

        for line_num, import_line in import_lines:
            # Determine import type
            if 'from .' in import_line or 'from src.' in import_line:
                import_type = 'local'
            else:
                # Extract module name
                if import_line.startswith('from '):
                    module = import_line.split(' ', 2)[1].split('.')[0]
                else:
                    module = import_line.split(' ', 1)[1].split('.')[0]

                if module in stdlib_modules:
                    import_type = 'stdlib'
                else:
                    import_type = 'third_party'

            # Check ordering
            if current_group == 'stdlib' and import_type in ['third_party', 'local']:
                current_group = import_type
            elif current_group == 'third_party' and import_type == 'local':
                current_group = 'local'
            elif import_type == 'stdlib' and current_group in ['third_party', 'local']:
                issues.append({
                    'line': line_num,
                    'issue': f'Standard library import after {current_group} imports',
                    'import': import_line
                })
            elif import_type == 'third_party' and current_group == 'local':
                issues.append({
                    'line': line_num,
                    'issue': 'Third-party import after local imports',
                    'import': import_line
                })

            last_import_line = line_num

        return {
            'organized': len(issues) == 0,
            'issues': issues,
            'total_imports': len(import_lines)
        }

    except Exception as e:
        return {'organized': False, 'issues': [{'error': str(e)}], 'total_imports': 0}

def analyze_codebase_imports_and_types() -> Dict[str, Any]:
    """Analyze imports and type hints across the entire codebase."""
    results = {
        'files_analyzed': 0,
        'files_with_errors': 0,
        'import_organization': {'well_organized': 0, 'needs_fixing': 0},
        'type_coverage': {
            'total_functions': 0,
            'functions_with_return_hints': 0,
            'total_params': 0,
            'params_with_hints': 0
        },
        'problematic_files': [],
        'top_issues': []
    }

    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')

                # Analyze file
                analysis = analyze_file_imports_and_types(file_path)
                results['files_analyzed'] += 1

                if 'error' in analysis:
                    results['files_with_errors'] += 1
                    continue

                # Check import organization
                org_check = check_import_organization(file_path)
                if org_check['organized']:
                    results['import_organization']['well_organized'] += 1
                else:
                    results['import_organization']['needs_fixing'] += 1
                    if len(org_check['issues']) > 3:  # Files with many import issues
                        results['problematic_files'].append({
                            'file': relative_path,
                            'type': 'import_organization',
                            'issue_count': len(org_check['issues'])
                        })

                # Aggregate type hint coverage
                th = analysis['type_hints']
                results['type_coverage']['total_functions'] += th['total_functions']
                results['type_coverage']['functions_with_return_hints'] += th['functions_with_return_hints']
                results['type_coverage']['total_params'] += th['total_params']
                results['type_coverage']['params_with_hints'] += th['params_with_hints']

                # Find files with poor type coverage
                if th['total_functions'] > 3 and th['return_hint_coverage'] < 0.5:
                    results['problematic_files'].append({
                        'file': relative_path,
                        'type': 'poor_type_coverage',
                        'return_coverage': th['return_hint_coverage'],
                        'param_coverage': th['param_hint_coverage']
                    })

    # Calculate overall coverage
    tc = results['type_coverage']
    tc['overall_return_coverage'] = tc['functions_with_return_hints'] / tc['total_functions'] if tc['total_functions'] > 0 else 0
    tc['overall_param_coverage'] = tc['params_with_hints'] / tc['total_params'] if tc['total_params'] > 0 else 0

    # Sort problematic files
    results['problematic_files'].sort(key=lambda x: x.get('issue_count', 0) + (1 - x.get('return_coverage', 1)), reverse=True)

    return results

if __name__ == "__main__":
    print("Import Organization and Type Hint Analysis")
    print("=" * 50)

    results = analyze_codebase_imports_and_types()

    print(f"Files analyzed: {results['files_analyzed']}")
    print(f"Files with errors: {results['files_with_errors']}")

    print(f"\nImport Organization:")
    print(f"  Well organized: {results['import_organization']['well_organized']}")
    print(f"  Need fixing: {results['import_organization']['needs_fixing']}")
    print(f"  Organization score: {results['import_organization']['well_organized'] / results['files_analyzed']:.2%}")

    print(f"\nType Hint Coverage:")
    tc = results['type_coverage']
    print(f"  Functions: {tc['total_functions']}")
    print(f"  Return hint coverage: {tc['overall_return_coverage']:.2%}")
    print(f"  Parameter hint coverage: {tc['overall_param_coverage']:.2%}")

    print(f"\nTop Problematic Files:")
    for i, file_info in enumerate(results['problematic_files'][:10], 1):
        if file_info['type'] == 'import_organization':
            print(f"  {i}. {file_info['file']} - {file_info['issue_count']} import issues")
        else:
            print(f"  {i}. {file_info['file']} - Return: {file_info['return_coverage']:.1%}, Param: {file_info['param_coverage']:.1%}")