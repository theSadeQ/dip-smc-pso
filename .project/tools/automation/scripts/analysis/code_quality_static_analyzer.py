#======================================================================================\\\
#========================== code_quality_static_analyzer.py ===========================\\\
#======================================================================================\\\

"""Perform static analysis and code quality improvements for the codebase."""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Tuple

def analyze_line_length_compliance() -> Dict[str, Any]:
    """Analyze compliance with 90-character line length."""
    results = {
        'total_files': 0,
        'compliant_files': 0,
        'violations': [],
        'summary': {}
    }

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')
                results['total_files'] += 1

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    violations_in_file = []
                    for i, line in enumerate(lines, 1):
                        # Don't count trailing newline
                        line_length = len(line.rstrip('\n\r'))
                        if line_length > 90:
                            violations_in_file.append({
                                'line': i,
                                'length': line_length,
                                'content': line.strip()[:100] + '...' if len(line.strip()) > 100 else line.strip()
                            })

                    if violations_in_file:
                        results['violations'].append({
                            'file': relative_path,
                            'violation_count': len(violations_in_file),
                            'violations': violations_in_file[:5]  # Top 5 violations
                        })
                    else:
                        results['compliant_files'] += 1

                except Exception as e:
                    continue

    # Generate summary
    results['summary'] = {
        'compliance_rate': results['compliant_files'] / results['total_files'] if results['total_files'] > 0 else 0,
        'total_violations': sum(len(v['violations']) for v in results['violations']),
        'worst_offenders': sorted(results['violations'], key=lambda x: x['violation_count'], reverse=True)[:10]
    }

    return results

def analyze_docstring_coverage() -> Dict[str, Any]:
    """Analyze docstring coverage across the codebase."""
    results = {
        'total_files': 0,
        'functions_analyzed': 0,
        'functions_with_docstrings': 0,
        'classes_analyzed': 0,
        'classes_with_docstrings': 0,
        'files_missing_docstrings': []
    }

    docstring_pattern = re.compile(r'^\s*""".*?"""\s*$', re.MULTILINE | re.DOTALL)
    function_pattern = re.compile(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', re.MULTILINE)
    class_pattern = re.compile(r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)', re.MULTILINE)

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')
                results['total_files'] += 1

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Find functions and classes
                    functions = function_pattern.findall(content)
                    classes = class_pattern.findall(content)

                    results['functions_analyzed'] += len(functions)
                    results['classes_analyzed'] += len(classes)

                    # Count docstrings (simple heuristic)
                    docstring_count = len(docstring_pattern.findall(content))

                    # Estimate coverage (rough approximation)
                    total_definitions = len(functions) + len(classes)
                    if total_definitions > 0:
                        estimated_coverage = min(docstring_count / total_definitions, 1.0)
                        if estimated_coverage < 0.5 and total_definitions > 2:
                            results['files_missing_docstrings'].append({
                                'file': relative_path,
                                'functions': len(functions),
                                'classes': len(classes),
                                'docstrings': docstring_count,
                                'estimated_coverage': estimated_coverage
                            })

                        # Simple estimation
                        results['functions_with_docstrings'] += int(len(functions) * estimated_coverage)
                        results['classes_with_docstrings'] += int(len(classes) * estimated_coverage)

                except Exception as e:
                    continue

    return results

def analyze_import_complexity() -> Dict[str, Any]:
    """Analyze import complexity and potential issues."""
    results = {
        'total_files': 0,
        'complex_import_files': [],
        'circular_dependency_risks': [],
        'unused_import_candidates': []
    }

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')
                results['total_files'] += 1

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Count imports
                    import_count = len(re.findall(r'^\s*(import |from )', content, re.MULTILINE))

                    # Look for complex import patterns
                    if import_count > 20:
                        results['complex_import_files'].append({
                            'file': relative_path,
                            'import_count': import_count
                        })

                    # Look for potential circular dependencies
                    local_imports = re.findall(r'from\s+(src\.[a-zA-Z0-9_.]+)', content)
                    if len(local_imports) > 5:
                        results['circular_dependency_risks'].append({
                            'file': relative_path,
                            'local_import_count': len(local_imports),
                            'imports': local_imports[:5]
                        })

                except Exception as e:
                    continue

    return results

def analyze_error_handling() -> Dict[str, Any]:
    """Analyze error handling patterns."""
    results = {
        'total_files': 0,
        'files_with_try_except': 0,
        'bare_except_violations': [],
        'broad_except_violations': []
    }

    bare_except_pattern = re.compile(r'^\s*except\s*:\s*$', re.MULTILINE)
    broad_except_pattern = re.compile(r'^\s*except\s+Exception\s*:\s*$', re.MULTILINE)
    try_pattern = re.compile(r'^\s*try\s*:\s*$', re.MULTILINE)

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, '.')
                results['total_files'] += 1

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for try-except blocks
                    if try_pattern.search(content):
                        results['files_with_try_except'] += 1

                    # Check for bare except clauses
                    bare_excepts = bare_except_pattern.findall(content)
                    if bare_excepts:
                        results['bare_except_violations'].append({
                            'file': relative_path,
                            'count': len(bare_excepts)
                        })

                    # Check for broad except clauses
                    broad_excepts = broad_except_pattern.findall(content)
                    if broad_excepts:
                        results['broad_except_violations'].append({
                            'file': relative_path,
                            'count': len(broad_excepts)
                        })

                except Exception as e:
                    continue

    return results

def run_comprehensive_static_analysis() -> Dict[str, Any]:
    """Run comprehensive static analysis of the codebase."""
    print("Running comprehensive static analysis...")

    analysis_results = {
        'line_length': analyze_line_length_compliance(),
        'docstring_coverage': analyze_docstring_coverage(),
        'import_complexity': analyze_import_complexity(),
        'error_handling': analyze_error_handling()
    }

    # Calculate overall code quality score
    line_score = analysis_results['line_length']['summary']['compliance_rate']

    doc_functions = analysis_results['docstring_coverage']['functions_analyzed']
    doc_with_strings = analysis_results['docstring_coverage']['functions_with_docstrings']
    doc_score = doc_with_strings / doc_functions if doc_functions > 0 else 1.0

    error_files = analysis_results['error_handling']['total_files']
    error_violations = len(analysis_results['error_handling']['bare_except_violations'])
    error_score = max(0, 1 - (error_violations / error_files)) if error_files > 0 else 1.0

    overall_score = (line_score * 0.3 + doc_score * 0.4 + error_score * 0.3)

    analysis_results['quality_score'] = {
        'line_length_score': line_score,
        'docstring_score': doc_score,
        'error_handling_score': error_score,
        'overall_score': overall_score,
        'grade': 'A' if overall_score >= 0.9 else 'B' if overall_score >= 0.8 else 'C' if overall_score >= 0.7 else 'D'
    }

    return analysis_results

if __name__ == "__main__":
    print("Code Quality Static Analysis")
    print("=" * 50)

    results = run_comprehensive_static_analysis()

    # Line length analysis
    line_results = results['line_length']
    print(f"\nLine Length Compliance (90 chars):")
    print(f"  Total files: {line_results['total_files']}")
    print(f"  Compliant files: {line_results['compliant_files']}")
    print(f"  Compliance rate: {line_results['summary']['compliance_rate']:.1%}")
    print(f"  Total violations: {line_results['summary']['total_violations']}")

    if line_results['summary']['worst_offenders']:
        print(f"  Worst offenders:")
        for offender in line_results['summary']['worst_offenders'][:3]:
            print(f"    {offender['file']}: {offender['violation_count']} violations")

    # Docstring coverage
    doc_results = results['docstring_coverage']
    print(f"\nDocstring Coverage:")
    print(f"  Functions analyzed: {doc_results['functions_analyzed']}")
    print(f"  Functions with docstrings: {doc_results['functions_with_docstrings']}")
    if doc_results['functions_analyzed'] > 0:
        doc_coverage = doc_results['functions_with_docstrings'] / doc_results['functions_analyzed']
        print(f"  Function docstring coverage: {doc_coverage:.1%}")

    # Import complexity
    import_results = results['import_complexity']
    print(f"\nImport Complexity:")
    print(f"  Files with complex imports (>20): {len(import_results['complex_import_files'])}")
    print(f"  Circular dependency risks: {len(import_results['circular_dependency_risks'])}")

    # Error handling
    error_results = results['error_handling']
    print(f"\nError Handling:")
    print(f"  Files with try-except: {error_results['files_with_try_except']}")
    print(f"  Bare except violations: {len(error_results['bare_except_violations'])}")
    print(f"  Broad except violations: {len(error_results['broad_except_violations'])}")

    # Overall quality score
    quality = results['quality_score']
    print(f"\nCode Quality Score:")
    print(f"  Line length score: {quality['line_length_score']:.2f}")
    print(f"  Docstring score: {quality['docstring_score']:.2f}")
    print(f"  Error handling score: {quality['error_handling_score']:.2f}")
    print(f"  Overall score: {quality['overall_score']:.2f} (Grade: {quality['grade']})")