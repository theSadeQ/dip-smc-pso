"""Automated axe-core accessibility testing using Puppeteer."""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

# Critical pages to test for Wave 1 validation
PAGES = [
    ("homepage", "/", "Homepage with hero and navigation"),
    ("getting-started", "/guides/getting-started.html", "Getting Started guide (UI-004 code blocks)"),
    ("controller-api", "/reference/controllers/index.html", "Controller API reference (UI-002 metadata)"),
    ("smc-theory", "/guides/theory/smc-theory.html", "SMC Theory guide (comprehensive doc page)"),
    ("benchmarks", "/benchmarks/index.html", "Performance benchmarks (tables and charts)"),
]

BASE_URL = "http://localhost:9000"
OUTPUT_DIR = Path(__file__).resolve().parent
TIMEOUT_MS = 60_000

# axe-core CDN URL (latest stable version)
AXE_CORE_URL = "https://cdn.jsdelivr.net/npm/axe-core@4.8.2/axe.min.js"


async def run_axe_scan() -> dict:
    """Run axe-core accessibility scans on all critical pages."""
    results = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "wave": "Wave 1 - Foundations & Accessibility",
            "axe_version": "4.8.2",
            "pages_scanned": len(PAGES),
            "base_url": BASE_URL,
        },
        "pages": [],
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

        for name, path, description in PAGES:
            url = f"{BASE_URL}{path}"
            print(f"\n{'='*60}")
            print(f"Testing: {name}")
            print(f"URL: {url}")
            print(f"Description: {description}")
            print(f"{'='*60}")

            try:
                # Navigate to page
                print("Navigating...")
                await page.goto(url, wait_until="networkidle", timeout=TIMEOUT_MS)

                # Inject axe-core library
                print("Injecting axe-core...")
                await page.add_script_tag(url=AXE_CORE_URL)

                # Wait for axe-core to load
                await page.wait_for_function("typeof axe !== 'undefined'", timeout=5000)

                # Run axe-core scan
                print("Running accessibility scan...")
                axe_results = await page.evaluate("""
                    async () => {
                        const results = await axe.run({
                            resultTypes: ['violations', 'incomplete'],
                            rules: {
                                // Focus on WCAG 2.1 Level AA
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
                            }
                        });
                        return results;
                    }
                """)

                # Process violations by severity
                page_violations = {
                    "critical": [],
                    "serious": [],
                    "moderate": [],
                    "minor": [],
                }

                for violation in axe_results.get("violations", []):
                    impact = violation.get("impact", "minor")
                    simplified_violation = {
                        "id": violation["id"],
                        "impact": impact,
                        "description": violation["description"],
                        "help": violation["help"],
                        "helpUrl": violation["helpUrl"],
                        "nodes": len(violation.get("nodes", [])),
                    }
                    page_violations[impact].append(simplified_violation)

                # Update summary counts
                results["summary"]["critical_violations"] += len(page_violations["critical"])
                results["summary"]["serious_violations"] += len(page_violations["serious"])
                results["summary"]["moderate_violations"] += len(page_violations["moderate"])
                results["summary"]["minor_violations"] += len(page_violations["minor"])
                results["summary"]["total_violations"] += sum(len(v) for v in page_violations.values())

                page_result = {
                    "name": name,
                    "url": url,
                    "description": description,
                    "status": "PASS" if len(page_violations["critical"]) == 0 else "FAIL",
                    "violations": page_violations,
                    "violation_counts": {
                        "critical": len(page_violations["critical"]),
                        "serious": len(page_violations["serious"]),
                        "moderate": len(page_violations["moderate"]),
                        "minor": len(page_violations["minor"]),
                    },
                }

                results["pages"].append(page_result)

                # Print summary
                print("[OK] Scan complete")
                print(f"  Critical: {len(page_violations['critical'])}")
                print(f"  Serious:  {len(page_violations['serious'])}")
                print(f"  Moderate: {len(page_violations['moderate'])}")
                print(f"  Minor:    {len(page_violations['minor'])}")

                if page_violations["critical"]:
                    print("\n[WARN] CRITICAL VIOLATIONS FOUND:")
                    for v in page_violations["critical"]:
                        print(f"  - {v['id']}: {v['description']}")

            except Exception as exc:
                print(f"[FAIL] FAILED: {exc}")
                results["pages"].append({
                    "name": name,
                    "url": url,
                    "description": description,
                    "status": "ERROR",
                    "error": str(exc),
                })

        await browser.close()

    return results


async def generate_reports(results: dict) -> None:
    """Generate JSON and Markdown reports from axe scan results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON report
    json_path = OUTPUT_DIR / f"wave1-exit-report-{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[REPORT] JSON report saved: {json_path}")

    # Generate Markdown summary
    md_path = OUTPUT_DIR / f"wave1-exit-summary-{timestamp}.md"
    with open(md_path, "w") as f:
        f.write("# Wave 1 Accessibility Validation Report (axe-core)\n\n")
        f.write(f"**Date**: {results['metadata']['date']}\n")
        f.write(f"**Wave**: {results['metadata']['wave']}\n")
        f.write(f"**axe-core Version**: {results['metadata']['axe_version']}\n")
        f.write(f"**Pages Scanned**: {results['metadata']['pages_scanned']}\n\n")

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
        f.write("## Wave 1 Exit Criteria Assessment\n\n")
        if results['summary']['critical_violations'] == 0:
            f.write("[PASS] **PASS**: 0 critical violations (target met)\n\n")
        else:
            f.write(f"[FAIL] **FAIL**: {results['summary']['critical_violations']} critical violations found (target: 0)\n\n")

        # Per-page results
        f.write("## Per-Page Results\n\n")
        for page in results["pages"]:
            status_icon = "[PASS]" if page["status"] == "PASS" else "[FAIL]"
            f.write(f"### {status_icon} {page['name']}\n\n")
            f.write(f"**URL**: `{page['url']}`\n")
            f.write(f"**Description**: {page['description']}\n\n")

            if page["status"] == "ERROR":
                f.write(f"**Error**: {page['error']}\n\n")
                continue

            f.write("| Severity | Count |\n")
            f.write("|----------|-------|\n")
            f.write(f"| Critical | {page['violation_counts']['critical']} |\n")
            f.write(f"| Serious | {page['violation_counts']['serious']} |\n")
            f.write(f"| Moderate | {page['violation_counts']['moderate']} |\n")
            f.write(f"| Minor | {page['violation_counts']['minor']} |\n\n")

            # List critical violations if any
            if page["violations"]["critical"]:
                f.write("**Critical Violations**:\n\n")
                for v in page["violations"]["critical"]:
                    f.write(f"- **{v['id']}**: {v['description']}\n")
                    f.write(f"  - Impact: {v['impact']}\n")
                    f.write(f"  - Affected elements: {v['nodes']}\n")
                    f.write(f"  - [More info]({v['helpUrl']})\n\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        if results['summary']['critical_violations'] == 0:
            f.write("- All critical accessibility issues have been resolved\n")
            f.write("- Wave 1 exit criteria for axe-core validation: **MET**\n")
            f.write("- Ready to proceed to Wave 2\n")
        else:
            f.write(f"- {results['summary']['critical_violations']} critical violations must be resolved before Wave 2\n")
            f.write("- Review detailed JSON report for full violation details\n")
            f.write("- Re-run validation after fixes applied\n")

    print(f"[REPORT] Markdown report saved: {md_path}")


async def main() -> None:
    """Main execution function."""
    print("Starting Wave 1 Accessibility Validation (axe-core)")
    print(f"Base URL: {BASE_URL}")
    print(f"Pages to scan: {len(PAGES)}\n")

    results = await run_axe_scan()
    await generate_reports(results)

    print(f"\n{'='*60}")
    print("VALIDATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total violations: {results['summary']['total_violations']}")
    print(f"Critical violations: {results['summary']['critical_violations']}")
    print(f"\nExit Criteria: {'[PASS]' if results['summary']['critical_violations'] == 0 else '[FAIL]'}")


if __name__ == "__main__":
    asyncio.run(main())
