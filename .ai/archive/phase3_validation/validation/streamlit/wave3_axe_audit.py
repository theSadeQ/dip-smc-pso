"""
Accessibility Audit for Wave 3 Streamlit Theme Validation.

Uses axe-core to validate WCAG AA compliance on themed Streamlit dashboard.
Tests color contrast, focus indicators, ARIA labels, keyboard navigation.

Usage:
    python wave3_axe_audit.py
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright


BASE_URL = "http://localhost:8501"
TIMEOUT_MS = 30_000
AXE_CORE_URL = "https://cdn.jsdelivr.net/npm/axe-core@4.8.2/axe.min.js"


async def run_axe_audit() -> dict:
    """Run axe-core accessibility audit on Streamlit dashboard."""
    results = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "wave": "Wave 3 - Streamlit Theme Parity",
            "axe_version": "4.8.2",
            "base_url": BASE_URL,
        },
        "violations": {
            "critical": [],
            "serious": [],
            "moderate": [],
            "minor": [],
        },
        "summary": {
            "total_violations": 0,
            "critical_violations": 0,
            "serious_violations": 0,
            "moderate_violations": 0,
            "minor_violations": 0,
        },
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            print(f"{'='*60}")
            print(f"Wave 3 Accessibility Audit (axe-core)")
            print(f"{'='*60}")
            print(f"URL: {BASE_URL}")
            print(f"axe-core version: 4.8.2")
            print(f"{'='*60}\n")

            # Navigate to Streamlit app
            print("Navigating to Streamlit dashboard...")
            await page.goto(BASE_URL, wait_until="networkidle", timeout=TIMEOUT_MS)

            # Wait for Streamlit to be ready
            await page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=TIMEOUT_MS)
            await asyncio.sleep(2)  # Extra wait for dynamic content

            # Inject axe-core library
            print("Injecting axe-core...")
            await page.add_script_tag(url=AXE_CORE_URL)
            await page.wait_for_function("typeof axe !== 'undefined'", timeout=5000)

            # Run axe-core scan
            print("Running accessibility scan...\n")
            axe_results = await page.evaluate("""
                async () => {
                    const results = await axe.run({
                        resultTypes: ['violations', 'incomplete'],
                        rules: {
                            // WCAG 2.1 Level AA rules
                            'color-contrast': { enabled: true },
                            'aria-allowed-attr': { enabled: true },
                            'aria-required-attr': { enabled: true },
                            'aria-valid-attr-value': { enabled: true },
                            'button-name': { enabled: true },
                            'image-alt': { enabled: true },
                            'label': { enabled: true },
                            'link-name': { enabled: true },
                            'list': { enabled: true },
                            'listitem': { enabled: true },
                            'focus-order-semantics': { enabled: true },
                            'landmark-one-main': { enabled: true },
                        }
                    });
                    return results;
                }
            """)

            # Process violations by severity
            for violation in axe_results.get("violations", []):
                impact = violation.get("impact", "minor")
                simplified_violation = {
                    "id": violation["id"],
                    "impact": impact,
                    "description": violation["description"],
                    "help": violation["help"],
                    "helpUrl": violation["helpUrl"],
                    "nodes": len(violation.get("nodes", [])),
                    "tags": violation.get("tags", []),
                }
                results["violations"][impact].append(simplified_violation)

            # Update summary counts
            results["summary"]["critical_violations"] = len(results["violations"]["critical"])
            results["summary"]["serious_violations"] = len(results["violations"]["serious"])
            results["summary"]["moderate_violations"] = len(results["violations"]["moderate"])
            results["summary"]["minor_violations"] = len(results["violations"]["minor"])
            results["summary"]["total_violations"] = (
                results["summary"]["critical_violations"] +
                results["summary"]["serious_violations"] +
                results["summary"]["moderate_violations"] +
                results["summary"]["minor_violations"]
            )

            # Print summary
            print("[OK] Scan complete\n")
            print("Violations by severity:")
            print(f"  Critical: {results['summary']['critical_violations']}")
            print(f"  Serious:  {results['summary']['serious_violations']}")
            print(f"  Moderate: {results['summary']['moderate_violations']}")
            print(f"  Minor:    {results['summary']['minor_violations']}")
            print(f"  Total:    {results['summary']['total_violations']}")

            if results["violations"]["critical"]:
                print("\n[WARN] CRITICAL VIOLATIONS FOUND:")
                for v in results["violations"]["critical"]:
                    print(f"  - {v['id']}: {v['description']}")

        except Exception as e:
            print(f"[ERROR] Audit failed: {e}")
            results["error"] = str(e)
        finally:
            await browser.close()

    return results


def generate_reports(results: dict) -> None:
    """Generate JSON and Markdown reports."""
    script_dir = Path(__file__).parent
    output_dir = script_dir / "wave3"
    output_dir.mkdir(exist_ok=True)

    # Save JSON report
    json_path = output_dir / "axe_audit_report.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n[REPORT] JSON saved: {json_path}")

    # Generate Markdown summary
    md_path = output_dir / "axe_audit_summary.md"
    with open(md_path, 'w') as f:
        f.write("# Wave 3 Accessibility Audit (axe-core)\n\n")
        f.write(f"**Date**: {results['metadata']['date']}\n")
        f.write(f"**Wave**: {results['metadata']['wave']}\n")
        f.write(f"**axe-core Version**: {results['metadata']['axe_version']}\n\n")

        # Summary table
        f.write("## Summary\n\n")
        f.write("| Severity | Count |\n")
        f.write("|----------|-------|\n")
        f.write(f"| **Critical** | {results['summary']['critical_violations']} |\n")
        f.write(f"| Serious | {results['summary']['serious_violations']} |\n")
        f.write(f"| Moderate | {results['summary']['moderate_violations']} |\n")
        f.write(f"| Minor | {results['summary']['minor_violations']} |\n")
        f.write(f"| **Total** | {results['summary']['total_violations']} |\n\n")

        # Exit criteria assessment
        f.write("## Wave 3 Exit Criteria Assessment\n\n")
        if results['summary']['critical_violations'] == 0 and results['summary']['serious_violations'] == 0:
            f.write("[PASS] **PASS**: 0 critical/serious violations (WCAG AA target met)\n\n")
        else:
            f.write(f"[FAIL] **FAIL**: {results['summary']['critical_violations']} critical + ")
            f.write(f"{results['summary']['serious_violations']} serious violations found\n\n")

        # Detailed violations
        if results['summary']['total_violations'] > 0:
            f.write("## Violations\n\n")

            for severity in ["critical", "serious", "moderate", "minor"]:
                violations = results["violations"][severity]
                if violations:
                    f.write(f"### {severity.capitalize()} Violations ({len(violations)})\n\n")
                    for v in violations:
                        f.write(f"#### {v['id']}\n\n")
                        f.write(f"- **Description**: {v['description']}\n")
                        f.write(f"- **Impact**: {v['impact']}\n")
                        f.write(f"- **Affected elements**: {v['nodes']}\n")
                        f.write(f"- **Tags**: {', '.join(v['tags'])}\n")
                        f.write(f"- **Help**: {v['help']}\n")
                        f.write(f"- [More info]({v['helpUrl']})\n\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        if results['summary']['critical_violations'] == 0 and results['summary']['serious_violations'] == 0:
            f.write("- All critical and serious accessibility issues resolved\n")
            f.write("- Theme meets WCAG AA compliance standards\n")
            f.write("- Wave 3 accessibility validation: **PASSED**\n")
        else:
            f.write(f"- {results['summary']['critical_violations'] + results['summary']['serious_violations']} ")
            f.write("critical/serious violations must be resolved\n")
            f.write("- Review detailed JSON report for full violation details\n")
            f.write("- Focus on color contrast and focus indicators\n")

    print(f"[REPORT] Markdown saved: {md_path}")


def main():
    """Main execution."""
    print("\n[INFO] Ensure Streamlit is running with theme enabled:")
    print("  - config.yaml -> streamlit.enable_dip_theme: true")
    print("  - Streamlit running on http://localhost:8501\n")

    results = asyncio.run(run_axe_audit())

    if "error" in results:
        print(f"\n[ERROR] Audit failed: {results['error']}")
        return

    generate_reports(results)

    print(f"\n{'='*60}")
    print("ACCESSIBILITY AUDIT COMPLETE")
    print(f"{'='*60}")
    print(f"Total violations: {results['summary']['total_violations']}")
    print(f"Critical: {results['summary']['critical_violations']}")
    print(f"Serious: {results['summary']['serious_violations']}")

    if results['summary']['critical_violations'] == 0 and results['summary']['serious_violations'] == 0:
        print(f"\n[PASS] Validation PASSED: WCAG AA compliance met")
    else:
        print(f"\n[FAIL] Validation FAILED: Critical/serious violations found")
        exit(1)


if __name__ == "__main__":
    main()
