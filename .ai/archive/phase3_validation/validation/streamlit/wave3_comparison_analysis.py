"""
Comparison Analysis for Wave 3 Streamlit Theme Validation.

Aggregates results from all validation scripts:
- Token mapping (CSV)
- Visual regression (JSON)
- Accessibility audit (JSON)
- Performance metrics (JSON)

Generates comprehensive pass/fail validation summary.

Usage:
    python wave3_comparison_analysis.py
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

try:
    import pandas as pd
except ImportError:
    print("[ERROR] pandas not installed")
    print("Install with: pip install pandas")
    exit(1)


def load_token_mapping(csv_path: Path) -> Dict[str, Any]:
    """Load and analyze token mapping CSV."""
    result = {
        "status": "not_run",
        "total_tokens": 0,
        "categories": {},
        "pass": False
    }

    if not csv_path.exists():
        result["error"] = "Token mapping CSV not found"
        return result

    try:
        df = pd.read_csv(csv_path)
        result["total_tokens"] = len(df)
        result["categories"] = df['category'].value_counts().to_dict()
        result["status"] = "success"
        result["pass"] = result["total_tokens"] >= 18  # Expect 18 tokens minimum
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def load_visual_regression(json_path: Path) -> Dict[str, Any]:
    """Load and analyze visual regression results."""
    result = {
        "status": "not_run",
        "total_comparisons": 0,
        "extreme_changes": 0,
        "significant_changes": 0,
        "pass": False
    }

    if not json_path.exists():
        result["error"] = "Visual regression report not found"
        return result

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        summary = data.get("summary", {})
        result["total_comparisons"] = summary.get("total_comparisons", 0)
        result["successful"] = summary.get("successful", 0)
        result["extreme_changes"] = summary.get("extreme_changes", 0)
        result["significant_changes"] = summary.get("significant_changes", 0)
        result["moderate_changes"] = summary.get("moderate_changes", 0)
        result["minimal_changes"] = summary.get("minimal_changes", 0)
        result["status"] = "success"

        # Pass if 0 extreme changes
        result["pass"] = result["extreme_changes"] == 0

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def load_accessibility_audit(json_path: Path) -> Dict[str, Any]:
    """Load and analyze accessibility audit results."""
    result = {
        "status": "not_run",
        "critical_violations": 0,
        "serious_violations": 0,
        "total_violations": 0,
        "pass": False
    }

    if not json_path.exists():
        result["error"] = "Accessibility audit report not found"
        return result

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        summary = data.get("summary", {})
        result["critical_violations"] = summary.get("critical_violations", 0)
        result["serious_violations"] = summary.get("serious_violations", 0)
        result["moderate_violations"] = summary.get("moderate_violations", 0)
        result["minor_violations"] = summary.get("minor_violations", 0)
        result["total_violations"] = summary.get("total_violations", 0)
        result["status"] = "success"

        # Pass if 0 critical AND 0 serious violations (WCAG AA target)
        result["pass"] = (
            result["critical_violations"] == 0 and
            result["serious_violations"] == 0
        )

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def load_performance_metrics(json_path: Path) -> Dict[str, Any]:
    """Load and analyze performance metrics."""
    result = {
        "status": "not_run",
        "gzipped_bytes": 0,
        "gzipped_kb": 0.0,
        "target_bytes": 3072,
        "pass": False
    }

    if not json_path.exists():
        result["error"] = "Performance metrics not found"
        return result

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        css_size = data.get("css_size", {})
        result["gzipped_bytes"] = css_size.get("gzipped_bytes", 0)
        result["gzipped_kb"] = css_size.get("gzipped_kb", 0.0)
        result["uncompressed_bytes"] = css_size.get("uncompressed_bytes", 0)
        result["compression_ratio"] = css_size.get("compression_ratio", 0.0)
        result["target_bytes"] = css_size.get("target_gzipped_bytes", 3072)
        result["status"] = "success"

        # Pass if CSS <3KB gzipped
        result["pass"] = result["gzipped_bytes"] < result["target_bytes"]

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def run_comparison_analysis() -> Dict[str, Any]:
    """Run complete comparison analysis."""
    script_dir = Path(__file__).parent
    wave3_dir = script_dir / "wave3"

    print(f"{'='*60}")
    print(f"Wave 3 Comparison Analysis")
    print(f"{'='*60}\n")

    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "wave": "Wave 3 - Streamlit Theme Parity",
            "validation_dir": str(wave3_dir)
        },
        "validation_results": {
            "token_mapping": {},
            "visual_regression": {},
            "accessibility": {},
            "performance": {}
        },
        "overall_assessment": {
            "total_tests": 4,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_not_run": 0,
            "overall_pass": False
        }
    }

    # Load token mapping
    print("[1/4] Loading token mapping results...")
    token_mapping = load_token_mapping(wave3_dir / "token_mapping.csv")
    results["validation_results"]["token_mapping"] = token_mapping
    print(f"  Status: {token_mapping['status']}")
    print(f"  Total tokens: {token_mapping.get('total_tokens', 0)}")
    print(f"  Result: {'PASS ✓' if token_mapping['pass'] else 'FAIL ✗'}\n")

    # Load visual regression
    print("[2/4] Loading visual regression results...")
    visual_regression = load_visual_regression(wave3_dir / "visual_regression_report.json")
    results["validation_results"]["visual_regression"] = visual_regression
    print(f"  Status: {visual_regression['status']}")
    print(f"  Extreme changes: {visual_regression.get('extreme_changes', 'N/A')}")
    print(f"  Result: {'PASS ✓' if visual_regression['pass'] else 'FAIL ✗'}\n")

    # Load accessibility audit
    print("[3/4] Loading accessibility audit results...")
    accessibility = load_accessibility_audit(wave3_dir / "axe_audit_report.json")
    results["validation_results"]["accessibility"] = accessibility
    print(f"  Status: {accessibility['status']}")
    print(f"  Critical: {accessibility.get('critical_violations', 'N/A')}")
    print(f"  Serious: {accessibility.get('serious_violations', 'N/A')}")
    print(f"  Result: {'PASS ✓' if accessibility['pass'] else 'FAIL ✗'}\n")

    # Load performance metrics
    print("[4/4] Loading performance metrics...")
    performance = load_performance_metrics(wave3_dir / "performance_metrics.json")
    results["validation_results"]["performance"] = performance
    print(f"  Status: {performance['status']}")
    print(f"  CSS size: {performance.get('gzipped_kb', 'N/A')} KB gzipped")
    print(f"  Result: {'PASS ✓' if performance['pass'] else 'FAIL ✗'}\n")

    # Calculate overall assessment
    for category, data in results["validation_results"].items():
        if data["status"] == "success":
            if data["pass"]:
                results["overall_assessment"]["tests_passed"] += 1
            else:
                results["overall_assessment"]["tests_failed"] += 1
        elif data["status"] == "not_run":
            results["overall_assessment"]["tests_not_run"] += 1
        else:  # error
            results["overall_assessment"]["tests_failed"] += 1

    # Overall pass requires all tests to pass
    results["overall_assessment"]["overall_pass"] = (
        results["overall_assessment"]["tests_passed"] == 4 and
        results["overall_assessment"]["tests_failed"] == 0
    )

    return results


def generate_reports(results: Dict[str, Any]) -> None:
    """Generate JSON and Markdown summary reports."""
    script_dir = Path(__file__).parent
    output_dir = script_dir / "wave3"

    # Save JSON report
    json_path = output_dir / "validation_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[REPORT] JSON saved: {json_path}")

    # Generate Markdown summary
    md_path = output_dir / "VALIDATION_SUMMARY.md"
    with open(md_path, 'w') as f:
        f.write("# Wave 3 Streamlit Theme Parity - Validation Summary\n\n")
        f.write(f"**Date**: {results['metadata']['timestamp']}\n")
        f.write(f"**Wave**: {results['metadata']['wave']}\n\n")

        # Overall status
        f.write("## Overall Status\n\n")
        overall = results["overall_assessment"]
        status_icon = "[PASS]" if overall["overall_pass"] else "[FAIL]"
        f.write(f"{status_icon} **{'PASSED' if overall['overall_pass'] else 'FAILED'}**\n\n")

        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Tests Passed | {overall['tests_passed']}/{overall['total_tests']} |\n")
        f.write(f"| Tests Failed | {overall['tests_failed']}/{overall['total_tests']} |\n")
        f.write(f"| Tests Not Run | {overall['tests_not_run']}/{overall['total_tests']} |\n\n")

        # Detailed results by category
        f.write("## Validation Results by Category\n\n")

        # 1. Token Mapping
        f.write("### 1. Token Mapping\n\n")
        token_data = results["validation_results"]["token_mapping"]
        token_icon = "[PASS]" if token_data.get("pass") else "[FAIL]"
        f.write(f"{token_icon} **Status**: {token_data['status']}\n\n")
        if token_data["status"] == "success":
            f.write(f"- **Total Tokens**: {token_data['total_tokens']}\n")
            f.write(f"- **Categories**: {', '.join(token_data.get('categories', {}).keys())}\n")
            f.write(f"- **Exit Criteria**: ≥18 tokens mapped\n")
            f.write(f"- **Result**: {'Criteria met ✓' if token_data['pass'] else 'Criteria not met ✗'}\n\n")
        elif "error" in token_data:
            f.write(f"- **Error**: {token_data['error']}\n\n")

        # 2. Visual Regression
        f.write("### 2. Visual Regression Testing\n\n")
        visual_data = results["validation_results"]["visual_regression"]
        visual_icon = "[PASS]" if visual_data.get("pass") else "[FAIL]"
        f.write(f"{visual_icon} **Status**: {visual_data['status']}\n\n")
        if visual_data["status"] == "success":
            f.write(f"- **Total Comparisons**: {visual_data['total_comparisons']}\n")
            f.write(f"- **Extreme Changes (>50%)**: {visual_data['extreme_changes']}\n")
            f.write(f"- **Significant Changes (20-50%)**: {visual_data['significant_changes']}\n")
            f.write(f"- **Moderate Changes (5-20%)**: {visual_data['moderate_changes']}\n")
            f.write(f"- **Minimal Changes (<5%)**: {visual_data['minimal_changes']}\n")
            f.write(f"- **Exit Criteria**: 0 extreme changes\n")
            f.write(f"- **Result**: {'Criteria met ✓' if visual_data['pass'] else 'Criteria not met ✗'}\n\n")
        elif "error" in visual_data:
            f.write(f"- **Error**: {visual_data['error']}\n\n")

        # 3. Accessibility
        f.write("### 3. Accessibility (WCAG AA)\n\n")
        a11y_data = results["validation_results"]["accessibility"]
        a11y_icon = "[PASS]" if a11y_data.get("pass") else "[FAIL]"
        f.write(f"{a11y_icon} **Status**: {a11y_data['status']}\n\n")
        if a11y_data["status"] == "success":
            f.write(f"- **Critical Violations**: {a11y_data['critical_violations']}\n")
            f.write(f"- **Serious Violations**: {a11y_data['serious_violations']}\n")
            f.write(f"- **Moderate Violations**: {a11y_data['moderate_violations']}\n")
            f.write(f"- **Minor Violations**: {a11y_data['minor_violations']}\n")
            f.write(f"- **Total Violations**: {a11y_data['total_violations']}\n")
            f.write(f"- **Exit Criteria**: 0 critical + 0 serious violations\n")
            f.write(f"- **Result**: {'Criteria met ✓' if a11y_data['pass'] else 'Criteria not met ✗'}\n\n")
        elif "error" in a11y_data:
            f.write(f"- **Error**: {a11y_data['error']}\n\n")

        # 4. Performance
        f.write("### 4. Performance (CSS Size)\n\n")
        perf_data = results["validation_results"]["performance"]
        perf_icon = "[PASS]" if perf_data.get("pass") else "[FAIL]"
        f.write(f"{perf_icon} **Status**: {perf_data['status']}\n\n")
        if perf_data["status"] == "success":
            f.write(f"- **Gzipped Size**: {perf_data['gzipped_bytes']} bytes ({perf_data['gzipped_kb']} KB)\n")
            f.write(f"- **Uncompressed Size**: {perf_data['uncompressed_bytes']} bytes\n")
            f.write(f"- **Compression Ratio**: {perf_data['compression_ratio']}x\n")
            f.write(f"- **Exit Criteria**: <3072 bytes (3 KB) gzipped\n")
            f.write(f"- **Result**: {'Criteria met ✓' if perf_data['pass'] else 'Criteria not met ✗'}\n\n")
        elif "error" in perf_data:
            f.write(f"- **Error**: {perf_data['error']}\n\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        if overall["overall_pass"]:
            f.write("**ALL VALIDATION CHECKS PASSED** ✓\n\n")
            f.write("The Streamlit theme implementation successfully meets all exit criteria:\n")
            f.write("- Token mapping complete\n")
            f.write("- Visual parity verified\n")
            f.write("- Accessibility standards met (WCAG AA)\n")
            f.write("- Performance budget satisfied\n\n")
            f.write("**Next Steps:**\n")
            f.write("1. Review detailed validation reports for any minor issues\n")
            f.write("2. Document integration guide for other projects\n")
            f.write("3. Mark Wave 3 as complete in CHANGELOG.md\n")
        else:
            f.write("**VALIDATION FAILURES DETECTED** ✗\n\n")
            failed_categories = [
                cat for cat, data in results["validation_results"].items()
                if not data.get("pass", False)
            ]
            f.write(f"Failed categories: {', '.join(failed_categories)}\n\n")
            f.write("**Required Actions:**\n")
            for category in failed_categories:
                data = results["validation_results"][category]
                f.write(f"\n**{category.replace('_', ' ').title()}:**\n")

                if category == "visual_regression" and data.get("extreme_changes", 0) > 0:
                    f.write(f"- Fix {data['extreme_changes']} extreme visual changes\n")
                    f.write("- Review `wave3/diffs/` for pixel difference images\n")

                if category == "accessibility":
                    crit = data.get("critical_violations", 0)
                    ser = data.get("serious_violations", 0)
                    if crit > 0:
                        f.write(f"- Resolve {crit} critical accessibility violations\n")
                    if ser > 0:
                        f.write(f"- Resolve {ser} serious accessibility violations\n")
                    f.write("- Review `wave3/axe_audit_report.json` for details\n")

                if category == "performance" and data.get("gzipped_bytes", 0) >= data.get("target_bytes", 3072):
                    overage = data["gzipped_bytes"] - data["target_bytes"]
                    f.write(f"- Reduce CSS size by {overage} bytes\n")
                    f.write("- Optimize selectors or reduce rules\n")

                if category == "token_mapping" and data.get("total_tokens", 0) < 18:
                    missing = 18 - data.get("total_tokens", 0)
                    f.write(f"- Add {missing} missing token mappings\n")

        # References
        f.write("\n## References\n\n")
        f.write("**Detailed Reports:**\n")
        f.write("- Token Mapping: `wave3/token_mapping.csv`\n")
        f.write("- Visual Regression: `wave3/visual_regression_summary.md`\n")
        f.write("- Accessibility: `wave3/axe_audit_summary.md`\n")
        f.write("- Performance: `wave3/performance_summary.md`\n\n")

        f.write("**Exit Criteria (from Phase 3 Plan):**\n")
        f.write("- Token mapping: All 18 tokens correctly mapped\n")
        f.write("- Visual regression: 0 extreme changes (>50% pixel difference)\n")
        f.write("- Accessibility: 0 critical/serious violations (WCAG AA)\n")
        f.write("- Performance: CSS <3KB gzipped\n")

    print(f"[REPORT] Markdown saved: {md_path}")


def main():
    """Main execution."""
    try:
        results = run_comparison_analysis()
        generate_reports(results)

        print(f"\n{'='*60}")
        print("COMPARISON ANALYSIS COMPLETE")
        print(f"{'='*60}")
        print(f"Overall Status: {'PASSED ✓' if results['overall_assessment']['overall_pass'] else 'FAILED ✗'}")
        print(f"Tests Passed: {results['overall_assessment']['tests_passed']}/4")
        print(f"Tests Failed: {results['overall_assessment']['tests_failed']}/4")

        if not results['overall_assessment']['overall_pass']:
            print("\n[WARN] Some validation checks failed. Review VALIDATION_SUMMARY.md for details.")
            exit(1)
        else:
            print("\n[SUCCESS] All validation checks passed!")

    except Exception as e:
        print(f"\n[ERROR] Comparison analysis failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
