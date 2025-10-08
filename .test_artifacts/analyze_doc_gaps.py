"""
Comprehensive documentation gap analysis by type.
Categorizes gaps into P0 (API docs), P1 (math proofs), P2 (examples), P3 (outdated refs).
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
import subprocess


def scan_p1_incomplete_math_proofs(docs_path: Path) -> List[Dict[str, Any]]:
    """Scan for incomplete mathematical proofs and derivations."""
    issues = []

    # Patterns indicating incomplete proofs
    patterns = [
        (r'proof\s*:\s*(tbd|todo|omitted|pending|incomplete)', 'proof_missing', 'high'),
        (r'theorem.*tbd', 'theorem_incomplete', 'high'),
        (r'derivation.*tbd', 'derivation_missing', 'medium'),
        (r'convergence.*analysis.*tbd', 'convergence_proof_missing', 'high'),
        (r'stability.*proof.*tbd', 'stability_proof_missing', 'critical'),
        (r'lyapunov.*tbd', 'lyapunov_proof_missing', 'critical'),
        (r'\[proof\s+needed\]', 'proof_needed', 'high'),
        (r'\[derivation\s+needed\]', 'derivation_needed', 'medium'),
        (r'TODO.*proof', 'proof_todo', 'high'),
        (r'FIXME.*stability', 'stability_fixme', 'critical'),
        (r'mathematical\s+foundation.*incomplete', 'foundation_incomplete', 'high'),
    ]

    theory_files = [
        'theory/*.md',
        'mathematical_foundations/*.md',
        'presentation/*.md',
    ]

    for pattern in theory_files:
        for filepath in docs_path.glob(pattern):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    for regex, issue_type, severity in patterns:
                        if re.search(regex, line_lower, re.IGNORECASE):
                            # Extract context
                            context = line.strip()[:100]
                            issues.append({
                                "file": str(filepath),
                                "line": line_num,
                                "type": issue_type,
                                "context": context,
                                "severity": severity,
                                "impact": f"Mathematical {issue_type.replace('_', ' ')} in theory documentation"
                            })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return issues


def scan_p2_missing_examples(docs_path: Path) -> List[Dict[str, Any]]:
    """Scan for missing code examples in documentation."""
    issues = []

    patterns = [
        (r'example\s*:\s*(tbd|todo|pending|coming soon)', 'example_missing', 'medium'),
        (r'```\s*python\s*\n\s*#\s*TODO', 'code_example_todo', 'medium'),
        (r'usage\s+example.*tbd', 'usage_example_missing', 'high'),
        (r'\[example\s+needed\]', 'example_needed', 'medium'),
        (r'see\s+example.*\(not\s+yet\s+available\)', 'example_unavailable', 'medium'),
        (r'TODO.*example', 'example_todo', 'medium'),
        (r'placeholder\s+example', 'example_placeholder', 'low'),
    ]

    doc_patterns = [
        'tutorials/*.md',
        'examples/*.md',
        'guides/*.md',
        'how-to/*.md',
        'factory/*.md',
        'technical/*.md',
    ]

    for pattern in doc_patterns:
        for filepath in docs_path.glob(pattern):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    for regex, issue_type, severity in patterns:
                        if re.search(regex, line_lower, re.IGNORECASE):
                            context = line.strip()[:100]
                            issues.append({
                                "file": str(filepath),
                                "line": line_num,
                                "type": issue_type,
                                "context": context,
                                "severity": severity,
                                "impact": f"Missing {issue_type.replace('_', ' ')} in user documentation"
                            })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return issues


def scan_p3_outdated_references(docs_path: Path, src_path: Path) -> List[Dict[str, Any]]:
    """Scan for outdated API references in documentation."""
    issues = []

    # Build list of current API classes and functions
    current_apis = set()
    for py_file in src_path.glob('**/*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract class names
                class_matches = re.findall(r'class\s+(\w+)', content)
                current_apis.update(class_matches)
        except:
            pass

    # Known deprecated APIs (from git history or changelogs)
    deprecated_apis = {
        'SimpleDynamics': 'SimplifiedDynamicsModel',
        'BasicController': 'ClassicalSMC',
        'PSOOptimizer': 'EnhancedPSOFactory',
        # Add more as discovered
    }

    # Scan documentation for references to deprecated APIs
    for filepath in docs_path.glob('**/*.md'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                for old_api, new_api in deprecated_apis.items():
                    if old_api in line and '`' in line:  # Likely a code reference
                        issues.append({
                            "file": str(filepath),
                            "line": line_num,
                            "type": "deprecated_api_reference",
                            "old_reference": old_api,
                            "current_reference": new_api,
                            "severity": "low",
                            "impact": f"Documentation references deprecated API '{old_api}' instead of '{new_api}'"
                        })
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    # Look for generic outdated markers
    outdated_patterns = [
        (r'deprecated', 'deprecated_content', 'medium'),
        (r'obsolete', 'obsolete_content', 'medium'),
        (r'no longer supported', 'unsupported_reference', 'high'),
        (r'old\s+api', 'old_api_reference', 'medium'),
    ]

    for filepath in docs_path.glob('**/*.md'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                for regex, issue_type, severity in outdated_patterns:
                    if re.search(regex, line_lower, re.IGNORECASE):
                        context = line.strip()[:100]
                        if 'deprecated' not in context.lower():  # Avoid duplicates
                            continue
                        issues.append({
                            "file": str(filepath),
                            "line": line_num,
                            "type": issue_type,
                            "context": context,
                            "severity": severity,
                            "impact": f"Documentation contains {issue_type.replace('_', ' ')}"
                        })
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    return issues


def analyze_general_todos_in_docs(docs_path: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Analyze general TODO/FIXME markers and categorize them."""
    categorized = {
        'p1_math': [],
        'p2_examples': [],
        'p3_general': []
    }

    todo_pattern = r'(TODO|FIXME|XXX|HACK|NOTE|OPTIMIZE)[\s:]*(.{0,100})'

    for filepath in docs_path.glob('**/*.md'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                match = re.search(todo_pattern, line, re.IGNORECASE)
                if match:
                    marker = match.group(1)
                    context = match.group(2).strip()

                    # Categorize by context
                    line_lower = line.lower()
                    if any(kw in line_lower for kw in ['proof', 'theorem', 'derivation', 'stability', 'convergence', 'lyapunov']):
                        category = 'p1_math'
                        severity = 'high'
                    elif any(kw in line_lower for kw in ['example', 'tutorial', 'demo', 'usage']):
                        category = 'p2_examples'
                        severity = 'medium'
                    else:
                        category = 'p3_general'
                        severity = 'low'

                    categorized[category].append({
                        "file": str(filepath),
                        "line": line_num,
                        "type": f"todo_{marker.lower()}",
                        "context": context[:100],
                        "severity": severity,
                        "impact": f"{marker} marker in documentation"
                    })
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    return categorized


def main():
    """Main analysis function."""
    base_path = Path(r"D:\Projects\main")
    docs_path = base_path / "docs"
    src_path = base_path / "src"

    print("=" * 80)
    print("DOCUMENTATION GAP ANALYSIS BY TYPE")
    print("=" * 80)

    # P0 already done by separate script
    print("\n[P0] Loading API documentation analysis...")
    try:
        with open(base_path / ".test_artifacts" / "p0_api_docs_analysis.json", 'r') as f:
            p0_data = json.load(f)
            p0_issues = p0_data['p0_missing_api_docs']
    except:
        p0_issues = []
    print(f"  Found {len(p0_issues)} API documentation issues")

    # P1: Incomplete mathematical proofs
    print("\n[P1] Scanning for incomplete mathematical proofs...")
    p1_issues = scan_p1_incomplete_math_proofs(docs_path)
    print(f"  Found {len(p1_issues)} incomplete math proofs")

    # P2: Missing code examples
    print("\n[P2] Scanning for missing code examples...")
    p2_issues = scan_p2_missing_examples(docs_path)
    print(f"  Found {len(p2_issues)} missing examples")

    # P3: Outdated API references
    print("\n[P3] Scanning for outdated API references...")
    p3_issues = scan_p3_outdated_references(docs_path, src_path)
    print(f"  Found {len(p3_issues)} outdated references")

    # General TODO analysis
    print("\n[TODOS] Analyzing general TODO markers...")
    todo_categorized = analyze_general_todos_in_docs(docs_path)
    print(f"  Math-related TODOs: {len(todo_categorized['p1_math'])}")
    print(f"  Example-related TODOs: {len(todo_categorized['p2_examples'])}")
    print(f"  General TODOs: {len(todo_categorized['p3_general'])}")

    # Merge TODO analysis into main categories
    p1_issues.extend(todo_categorized['p1_math'])
    p2_issues.extend(todo_categorized['p2_examples'])
    p3_issues.extend(todo_categorized['p3_general'])

    # Compile full analysis
    full_analysis = {
        "analysis_date": "2025-10-07",
        "summary": {
            "p0_critical_api_docs": len(p0_issues),
            "p1_incomplete_math_proofs": len(p1_issues),
            "p2_missing_examples": len(p2_issues),
            "p3_outdated_references": len(p3_issues),
            "total_issues": len(p0_issues) + len(p1_issues) + len(p2_issues) + len(p3_issues)
        },
        "p0_missing_api_docs": p0_issues[:100],  # Limit for JSON size
        "p1_incomplete_math_proofs": p1_issues,
        "p2_missing_examples": p2_issues,
        "p3_outdated_references": p3_issues
    }

    # Save JSON
    output_json = base_path / "docs" / "TODO_ANALYSIS_BY_DOCTYPE_2025-10-07.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(full_analysis, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Analysis complete. Results saved to:")
    print(f"  {output_json}")
    print(f"\nTotal issues found: {full_analysis['summary']['total_issues']}")
    print(f"  P0 (Critical API docs): {len(p0_issues)}")
    print(f"  P1 (Incomplete math): {len(p1_issues)}")
    print(f"  P2 (Missing examples): {len(p2_issues)}")
    print(f"  P3 (Outdated refs): {len(p3_issues)}")

    return full_analysis


if __name__ == "__main__":
    main()
