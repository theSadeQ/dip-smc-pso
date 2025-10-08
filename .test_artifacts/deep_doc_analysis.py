"""
Deep documentation analysis with enhanced categorization.
Provides detailed metrics and top priority items.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def estimate_effort_hours(issue_type: str, count: int = 1) -> float:
    """Estimate effort in hours based on issue type."""
    effort_map = {
        # P0: API Documentation
        'class_docstring_missing': 0.5,  # 30 min per class
        'method_docstring_missing': 0.25,  # 15 min per method
        'function_docstring_missing': 0.3,  # 18 min per function
        'parameter_docs_missing': 0.2,  # 12 min to add params section
        'return_docs_missing': 0.1,  # 6 min to add returns section

        # P1: Mathematical Proofs
        'proof_missing': 2.0,  # 2 hours per proof
        'stability_proof_missing': 3.0,  # 3 hours for stability
        'convergence_proof_missing': 2.5,  # 2.5 hours for convergence
        'lyapunov_proof_missing': 4.0,  # 4 hours for Lyapunov
        'theorem_incomplete': 2.0,
        'derivation_missing': 1.5,
        'todo_fixme': 0.5,
        'todo_todo': 0.5,

        # P2: Code Examples
        'example_missing': 0.75,  # 45 min per example
        'code_example_todo': 0.5,
        'usage_example_missing': 1.0,
        'todo_todo': 0.5,

        # P3: Outdated References
        'deprecated_api_reference': 0.2,  # 12 min to update reference
        'outdated_content': 0.3,
        'deprecated_content': 0.25,
    }

    base_effort = effort_map.get(issue_type, 0.5)
    return base_effort * count


def analyze_p0_details(p0_issues: List[Dict]) -> Dict[str, Any]:
    """Detailed analysis of P0 API documentation gaps."""
    by_type = defaultdict(int)
    by_severity = defaultdict(int)
    by_file = defaultdict(int)

    for issue in p0_issues:
        by_type[issue['type']] += 1
        by_severity[issue['severity']] += 1
        file_path = issue['file']
        # Shorten path for readability
        short_path = file_path.replace('D:\\Projects\\main\\src\\', 'src/')
        by_file[short_path] += 1

    total_effort = sum(estimate_effort_hours(t, c) for t, c in by_type.items())

    # Find worst offenders
    worst_files = sorted(by_file.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'total_issues': len(p0_issues),
        'by_type': dict(by_type),
        'by_severity': dict(by_severity),
        'estimated_effort_hours': round(total_effort, 1),
        'worst_files': worst_files
    }


def analyze_p1_details(p1_issues: List[Dict]) -> Dict[str, Any]:
    """Detailed analysis of P1 mathematical proof gaps."""
    by_type = defaultdict(int)
    by_severity = defaultdict(int)
    by_file = defaultdict(int)

    for issue in p1_issues:
        by_type[issue['type']] += 1
        by_severity[issue['severity']] += 1
        file_path = issue['file']
        short_path = file_path.replace('D:\\Projects\\main\\docs\\', 'docs/')
        by_file[short_path] += 1

    total_effort = sum(estimate_effort_hours(t, c) for t, c in by_type.items())

    worst_files = sorted(by_file.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'total_issues': len(p1_issues),
        'by_type': dict(by_type),
        'by_severity': dict(by_severity),
        'estimated_effort_hours': round(total_effort, 1),
        'worst_files': worst_files
    }


def analyze_p2_details(p2_issues: List[Dict]) -> Dict[str, Any]:
    """Detailed analysis of P2 missing examples."""
    by_type = defaultdict(int)
    by_file = defaultdict(int)

    for issue in p2_issues:
        by_type[issue['type']] += 1
        file_path = issue['file']
        short_path = file_path.replace('D:\\Projects\\main\\docs\\', 'docs/')
        by_file[short_path] += 1

    total_effort = sum(estimate_effort_hours(t, c) for t, c in by_type.items())

    worst_files = sorted(by_file.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'total_issues': len(p2_issues),
        'by_type': dict(by_type),
        'estimated_effort_hours': round(total_effort, 1),
        'worst_files': worst_files
    }


def analyze_p3_details(p3_issues: List[Dict]) -> Dict[str, Any]:
    """Detailed analysis of P3 outdated references."""
    by_type = defaultdict(int)
    by_file = defaultdict(int)

    for issue in p3_issues:
        by_type[issue['type']] += 1
        file_path = issue['file']
        short_path = file_path.replace('D:\\Projects\\main\\docs\\', 'docs/')
        by_file[short_path] += 1

    total_effort = sum(estimate_effort_hours(t, c) for t, c in by_type.items())

    worst_files = sorted(by_file.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'total_issues': len(p3_issues),
        'by_type': dict(by_type),
        'estimated_effort_hours': round(total_effort, 1),
        'worst_files': worst_files
    }


def compute_top_priorities(all_issues: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
    """Compute top 20 priority items across all categories."""
    priority_items = []

    # Scoring: severity * impact_weight
    severity_scores = {
        'critical': 10,
        'high': 7,
        'medium': 4,
        'low': 2
    }

    impact_weights = {
        'class_docstring_missing': 5,
        'method_docstring_missing': 3,
        'stability_proof_missing': 10,
        'lyapunov_proof_missing': 10,
        'convergence_proof_missing': 8,
        'usage_example_missing': 6,
        'deprecated_api_reference': 2,
    }

    for category, issues in all_issues.items():
        for issue in issues:
            severity_score = severity_scores.get(issue.get('severity', 'low'), 2)
            impact_weight = impact_weights.get(issue.get('type', ''), 3)
            priority_score = severity_score * impact_weight

            # Shorten file path
            file_path = issue.get('file', '')
            short_path = file_path.replace('D:\\Projects\\main\\', '')

            priority_items.append({
                'category': category,
                'priority_score': priority_score,
                'file': short_path,
                'line': issue.get('line', 0),
                'type': issue.get('type', 'unknown'),
                'api_name': issue.get('api_name', issue.get('context', ''))[:60],
                'impact': issue.get('impact', '')[:100],
                'effort_hours': estimate_effort_hours(issue.get('type', ''))
            })

    # Sort by priority score descending
    priority_items.sort(key=lambda x: x['priority_score'], reverse=True)

    return priority_items[:20]


def main():
    """Main deep analysis function."""
    base_path = Path(r"D:\Projects\main")
    json_file = base_path / "docs" / "TODO_ANALYSIS_BY_DOCTYPE_2025-10-07.json"

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("=" * 80)
    print("DEEP DOCUMENTATION GAP ANALYSIS")
    print("=" * 80)

    # Detailed analysis
    p0_details = analyze_p0_details(data['p0_missing_api_docs'])
    p1_details = analyze_p1_details(data['p1_incomplete_math_proofs'])
    p2_details = analyze_p2_details(data['p2_missing_examples'])
    p3_details = analyze_p3_details(data['p3_outdated_references'])

    print(f"\nP0 Critical API Documentation: {p0_details['total_issues']} issues")
    print(f"  Effort: {p0_details['estimated_effort_hours']}h")
    print(f"  Breakdown: {dict(sorted(p0_details['by_type'].items(), key=lambda x: x[1], reverse=True))}")

    print(f"\nP1 Incomplete Math Proofs: {p1_details['total_issues']} issues")
    print(f"  Effort: {p1_details['estimated_effort_hours']}h")
    print(f"  Breakdown: {dict(sorted(p1_details['by_type'].items(), key=lambda x: x[1], reverse=True))}")

    print(f"\nP2 Missing Examples: {p2_details['total_issues']} issues")
    print(f"  Effort: {p2_details['estimated_effort_hours']}h")
    print(f"  Breakdown: {dict(sorted(p2_details['by_type'].items(), key=lambda x: x[1], reverse=True))}")

    print(f"\nP3 Outdated References: {p3_details['total_issues']} issues")
    print(f"  Effort: {p3_details['estimated_effort_hours']}h")
    print(f"  Breakdown: {dict(sorted(p3_details['by_type'].items(), key=lambda x: x[1], reverse=True))}")

    # Top priorities
    all_issues = {
        'p0': data['p0_missing_api_docs'],
        'p1': data['p1_incomplete_math_proofs'],
        'p2': data['p2_missing_examples'],
        'p3': data['p3_outdated_references']
    }

    top_priorities = compute_top_priorities(all_issues)

    # Enhanced JSON output
    enhanced_data = {
        **data,
        'detailed_analysis': {
            'p0_details': p0_details,
            'p1_details': p1_details,
            'p2_details': p2_details,
            'p3_details': p3_details
        },
        'top_20_priorities': top_priorities,
        'total_effort_hours': round(
            p0_details['estimated_effort_hours'] +
            p1_details['estimated_effort_hours'] +
            p2_details['estimated_effort_hours'] +
            p3_details['estimated_effort_hours'],
            1
        )
    }

    # Save enhanced JSON
    output_file = base_path / "docs" / "TODO_ANALYSIS_BY_DOCTYPE_2025-10-07.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Enhanced analysis saved to: {output_file}")
    print(f"\nTotal estimated effort: {enhanced_data['total_effort_hours']} hours")
    print(f"\nTop 10 Priority Items:")
    for i, item in enumerate(top_priorities[:10], 1):
        print(f"  {i}. [{item['category'].upper()}] {item['file']}:{item['line']}")
        print(f"     {item['type']} - {item['api_name']}")
        print(f"     Effort: {item['effort_hours']}h, Priority: {item['priority_score']}")


if __name__ == "__main__":
    main()
