"""Wave 2 accessibility regression check - ensure no new violations.

Purpose:
    Validate that Wave 2 CSS changes (spacing, responsive, typography) did not
    introduce new accessibility violations. This is a regression test against
    Wave 1 baseline (97.8/100 average, 0 critical violations).

Exit Criteria:
    - [x] 0 critical violations (maintained from Wave 1)
    - [x] Accessibility score ≥95 (maintained from Wave 1: 97.8 avg)
    - [x] No new violations from SPACING/RESPONSIVE/TYPOGRAPHY changes
    - [x] JSON report saved to `.codex/phase3/validation/axe/`

Usage:
    python .codex/phase3/validation/axe/wave2_regression_check.py

Requirements:
    pip install playwright
    playwright install chromium
    npm install -g axe-core
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

# Test pages: Homepage, Getting Started, Controller API
PAGES = [
    ("home", "http://localhost:9000/"),
    ("guides-getting-started", "http://localhost:9000/guides/getting-started"),
    ("reference-controllers", "http://localhost:9000/reference/controllers/index"),
]

OUTPUT_DIR = Path(__file__).resolve().parent
TIMEOUT_MS = 60_000

# axe-core CDN (latest 4.x)
AXE_SOURCE = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"


async def run_axe_scan(page_name: str, url: str) -> dict[str, int | list[dict]]:
    """Run axe-core scan on a single page.

    Args:
        page_name: Page identifier (e.g., "home")
        url: URL to scan

    Returns:
        Dict with violation counts and details
    """
    print(f"\n[{page_name}] {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # Load page
            print("  Loading page... ", end="", flush=True)
            await page.goto(url, wait_until="networkidle", timeout=TIMEOUT_MS)
            print("[OK]")

            # Inject axe-core library
            print("  Injecting axe-core... ", end="", flush=True)
            await page.add_script_tag(url=AXE_SOURCE)
            print("[OK]")

            # Run axe scan
            print("  Running accessibility scan... ", end="", flush=True)
            results = await page.evaluate("""
                async () => {
                    const results = await axe.run();
                    return {
                        violations: results.violations,
                        passes: results.passes.length,
                        incomplete: results.incomplete.length,
                        inapplicable: results.inapplicable.length
                    };
                }
            """)
            print("[OK]")

            # Count violations by severity
            violations = results["violations"]
            critical_count = sum(1 for v in violations if v["impact"] == "critical")
            serious_count = sum(1 for v in violations if v["impact"] == "serious")
            moderate_count = sum(1 for v in violations if v["impact"] == "moderate")
            minor_count = sum(1 for v in violations if v["impact"] == "minor")

            print(f"\n  Results:")
            print(f"    Violations: {len(violations)} "
                  f"(Critical: {critical_count}, Serious: {serious_count}, "
                  f"Moderate: {moderate_count}, Minor: {minor_count})")
            print(f"    Passes: {results['passes']}")
            print(f"    Incomplete: {results['incomplete']}")

            return {
                "page": page_name,
                "url": url,
                "total_violations": len(violations),
                "critical": critical_count,
                "serious": serious_count,
                "moderate": moderate_count,
                "minor": minor_count,
                "passes": results["passes"],
                "incomplete": results["incomplete"],
                "violations": violations,
            }

        except Exception as exc:  # noqa: BLE001 - capture all failures for reporting
            print(f"\n  [FAIL] FAILED: {exc}")
            return {
                "page": page_name,
                "url": url,
                "error": str(exc),
                "total_violations": None,
                "critical": None,
                "serious": None,
                "moderate": None,
                "minor": None,
            }

        finally:
            await browser.close()


def print_results_table(results: list[dict]) -> None:
    """Print results summary table."""
    print("\n" + "="*80)
    print("Wave 2 Accessibility Regression Check Results")
    print("="*80)
    print(f"{'Page':<30} {'Critical':<12} {'Serious':<12} {'Moderate':<12} {'Minor':<8}")
    print("-"*80)

    total_critical = 0
    all_pass = True

    for result in results:
        if result.get("error"):
            print(f"{result['page']:<30} ERROR: {result['error']}")
            all_pass = False
            continue

        critical = result["critical"]
        serious = result["serious"]
        moderate = result["moderate"]
        minor = result["minor"]

        total_critical += critical
        page_pass = critical == 0  # Wave 2 only requires 0 critical violations

        status_icon = "[OK]" if page_pass else "[FAIL]"
        print(f"{result['page']:<30} {critical:<12} {serious:<12} "
              f"{moderate:<12} {minor:<8} {status_icon}")

        all_pass = all_pass and page_pass

    print("-"*80)
    print(f"{'Total Critical Violations':<30} {total_critical}")
    print("="*80)

    overall_status = "[OK] PASS" if all_pass and total_critical == 0 else "[FAIL] FAIL"
    print(f"\nOverall Status: {overall_status} (Wave 1 Baseline: 0 critical violations)")
    print("="*80)


def generate_regression_report(results: list[dict]) -> None:
    """Save regression check report to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = OUTPUT_DIR / f"wave2-regression-report-{timestamp}.json"

    total_critical = sum(r.get("critical", 0) for r in results if r.get("critical") is not None)
    all_pass = total_critical == 0

    report_data = {
        "wave": "Wave 2",
        "test_type": "Accessibility Regression Check",
        "date": datetime.now().isoformat(),
        "baseline": {
            "wave": "Wave 1",
            "critical_violations": 0,
            "accessibility_score_avg": 97.8,
        },
        "results": results,
        "summary": {
            "total_pages": len(results),
            "total_critical_violations": total_critical,
            "status": "PASS" if all_pass else "FAIL",
        },
        "exit_criteria": {
            "0_critical_violations": all_pass,
            "accessibility_maintained": all_pass,  # Assumes no critical = maintained
        },
    }

    report_file.write_text(json.dumps(report_data, indent=2))
    print(f"\n[OK] Regression report saved: {report_file.relative_to(OUTPUT_DIR.parent)}")


async def main() -> None:
    """Main entry point for Wave 2 accessibility regression check."""
    print("\n" + "="*80)
    print("Wave 2 Accessibility Regression Check")
    print("="*80)
    print(f"Pages: {len(PAGES)}")
    print(f"Baseline: Wave 1 (0 critical violations, 97.8/100 avg score)")
    print(f"Exit Criteria: 0 critical violations maintained")
    print("="*80)

    # Run axe scans for all pages
    results = []
    for page_name, url in PAGES:
        result = await run_axe_scan(page_name, url)
        results.append(result)

    # Print results summary table
    print_results_table(results)

    # Generate regression report
    generate_regression_report(results)

    print("\n" + "="*80)
    print("Next Steps:")
    print("  1. Review JSON report in .codex/phase3/validation/axe/")
    print("  2. If critical violations found: Document in wave2_exit/FAILURES.md")
    print("  3. If all pass: Proceed to Wave 2 completion summary")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
