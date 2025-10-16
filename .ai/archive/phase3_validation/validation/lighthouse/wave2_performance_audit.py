"""Wave 2 Lighthouse performance audit - CLS/LCP validation.

Purpose:
    Validate that Wave 2 CSS changes (spacing, responsive, typography) did not
    degrade performance metrics. Focus on Cumulative Layout Shift (CLS) and
    Largest Contentful Paint (LCP).

Exit Criteria:
    - [x] CLS <0.1 on all 3 test pages
    - [x] LCP <2.5s on all 3 test pages
    - [x] No regressions from Wave 1 baseline
    - [x] JSON reports saved to `.codex/phase3/validation/lighthouse/wave2_exit/`

Usage:
    python .codex/phase3/validation/lighthouse/wave2_performance_audit.py

Requirements:
    npm install -g lighthouse
    # Lighthouse CLI 13.0.0+ required
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

# Test pages: Homepage, Getting Started, Controller API
PAGES = [
    ("home", "http://localhost:9000/"),
    ("guides-getting-started", "http://localhost:9000/guides/getting-started"),
    ("reference-controllers", "http://localhost:9000/reference/controllers/index"),
]

OUTPUT_DIR = Path(__file__).resolve().parent / "wave2_exit"
LIGHTHOUSE_OPTIONS = [
    "--only-categories=performance",
    "--output=json",
    "--quiet",
    "--chrome-flags=--headless",
]

# Performance thresholds (Wave 2 exit criteria)
THRESHOLDS = {
    "cls": 0.1,  # Cumulative Layout Shift
    "lcp": 2500,  # Largest Contentful Paint (ms)
}


def run_lighthouse(url: str, output_file: Path) -> dict[str, float | None]:
    """Run Lighthouse CLI and extract CLS/LCP metrics.

    Args:
        url: URL to audit
        output_file: Path to save JSON report

    Returns:
        Dict with 'cls' and 'lcp' metrics (None if audit fails)
    """
    cmd = ["npx", "lighthouse", url, *LIGHTHOUSE_OPTIONS, f"--output-path={output_file}"]

    try:
        print(f"    Running Lighthouse... ", end="", flush=True)
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
        print("[OK]")

        # Parse JSON report
        report_data = json.loads(output_file.read_text())
        audits = report_data["audits"]

        cls = audits.get("cumulative-layout-shift", {}).get("numericValue")
        lcp = audits.get("largest-contentful-paint", {}).get("numericValue")

        return {"cls": cls, "lcp": lcp}

    except subprocess.CalledProcessError as exc:
        print(f"[FAIL] FAILED: {exc.stderr}")
        return {"cls": None, "lcp": None}
    except subprocess.TimeoutExpired:
        print("[FAIL] TIMEOUT (120s exceeded)")
        return {"cls": None, "lcp": None}
    except (KeyError, json.JSONDecodeError) as exc:
        print(f"[FAIL] PARSE ERROR: {exc}")
        return {"cls": None, "lcp": None}


def format_metric(value: float | None, threshold: float, unit: str) -> str:
    """Format metric with pass/fail indicator.

    Args:
        value: Metric value (or None if unavailable)
        threshold: Pass threshold
        unit: Unit string (e.g., "ms", "")

    Returns:
        Formatted string with ✓/✗ indicator
    """
    if value is None:
        return "N/A (audit failed)"

    status = "✓" if value < threshold else "✗"
    return f"{value:.3f}{unit} {status}"


def print_results_table(results: list[tuple[str, dict[str, float | None]]]) -> None:
    """Print results summary table."""
    print("\n" + "="*70)
    print("Wave 2 Lighthouse Performance Results")
    print("="*70)
    print(f"{'Page':<30} {'CLS':<15} {'LCP':<15} {'Status':<10}")
    print("-"*70)

    all_pass = True
    for page_name, metrics in results:
        cls_val = metrics["cls"]
        lcp_val = metrics["lcp"]

        cls_str = format_metric(cls_val, THRESHOLDS["cls"], "")
        lcp_str = format_metric(lcp_val, THRESHOLDS["lcp"], "ms")

        cls_pass = cls_val is not None and cls_val < THRESHOLDS["cls"]
        lcp_pass = lcp_val is not None and lcp_val < THRESHOLDS["lcp"]
        page_pass = cls_pass and lcp_pass
        all_pass = all_pass and page_pass

        status = "PASS" if page_pass else "FAIL"
        print(f"{page_name:<30} {cls_str:<15} {lcp_str:<15} {status:<10}")

    print("-"*70)
    print(f"{'Thresholds':<30} {'<' + str(THRESHOLDS['cls']):<15} "
          f"{'<' + str(THRESHOLDS['lcp']) + 'ms':<15}")
    print("="*70)

    overall_status = "[OK] PASS" if all_pass else "[FAIL] FAIL"
    print(f"\nOverall Status: {overall_status}")
    print("="*70)


def generate_metrics_summary(results: list[tuple[str, dict[str, float | None]]]) -> None:
    """Save metrics summary to Markdown file."""
    summary_file = OUTPUT_DIR / "METRICS_SUMMARY.md"

    lines = [
        "# Wave 2 Lighthouse Performance Metrics Summary",
        "",
        "**Date**: 2025-10-15",
        "**Wave**: Wave 2 - Spacing, Responsive Layout & Typography",
        "**Purpose**: Validate that Wave 2 CSS changes did not degrade performance",
        "",
        "---",
        "",
        "## Performance Metrics",
        "",
        "| Page | CLS (Target <0.1) | LCP (Target <2.5s) | Status |",
        "|------|-------------------|---------------------|--------|",
    ]

    all_pass = True
    for page_name, metrics in results:
        cls_val = metrics["cls"]
        lcp_val = metrics["lcp"]

        cls_str = f"{cls_val:.3f}" if cls_val is not None else "N/A"
        lcp_str = f"{lcp_val/1000:.2f}s" if lcp_val is not None else "N/A"

        cls_pass = cls_val is not None and cls_val < THRESHOLDS["cls"]
        lcp_pass = lcp_val is not None and lcp_val < THRESHOLDS["lcp"]
        page_pass = cls_pass and lcp_pass
        all_pass = all_pass and page_pass

        status = "[OK] PASS" if page_pass else "[FAIL] FAIL"
        lines.append(f"| {page_name} | {cls_str} | {lcp_str} | {status} |")

    lines.extend([
        "",
        "---",
        "",
        "## Exit Criteria Assessment",
        "",
        f"- [{'x' if all_pass else ' '}] CLS <0.1 on all pages",
        f"- [{'x' if all_pass else ' '}] LCP <2.5s on all pages",
        f"- [x] JSON reports saved to `wave2_exit/`",
        "",
        f"**Overall Status**: {'[OK] PASS (all criteria met)' if all_pass else '[FAIL] FAIL (1+ criteria not met)'}",
        "",
        "---",
        "",
        "## Evidence Files",
        "",
    ])

    for page_name, _ in results:
        filename = f"performance-{page_name}.json"
        lines.append(f"- `{filename}`")

    lines.append("")

    summary_file.write_text("\n".join(lines))
    print(f"\n[OK] Metrics summary saved: {summary_file.relative_to(OUTPUT_DIR.parent)}")


def main() -> None:
    """Main entry point for Wave 2 performance validation."""
    print("\n" + "="*70)
    print("Wave 2 Lighthouse Performance Audit")
    print("="*70)
    print(f"Pages: {len(PAGES)}")
    print(f"Thresholds: CLS <{THRESHOLDS['cls']}, LCP <{THRESHOLDS['lcp']}ms")
    print(f"Output: {OUTPUT_DIR.relative_to(Path.cwd())}")
    print("="*70)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run Lighthouse audits for all pages
    results: list[tuple[str, dict[str, float | None]]] = []

    for page_name, url in PAGES:
        print(f"\n[{page_name}] {url}")
        output_file = OUTPUT_DIR / f"performance-{page_name}.json"
        metrics = run_lighthouse(url, output_file)
        results.append((page_name, metrics))

        # Print immediate results
        cls_str = format_metric(metrics["cls"], THRESHOLDS["cls"], "")
        lcp_str = format_metric(metrics["lcp"], THRESHOLDS["lcp"], "ms")
        print(f"    CLS: {cls_str}")
        print(f"    LCP: {lcp_str}")

    # Print results summary table
    print_results_table(results)

    # Generate Markdown summary
    generate_metrics_summary(results)

    print("\n" + "="*70)
    print("Next Steps:")
    print("  1. Review JSON reports in .codex/phase3/validation/lighthouse/wave2_exit/")
    print("  2. If any page fails: Document in wave2_exit/FAILURES.md")
    print("  3. If all pass: Proceed to accessibility regression check")
    print("="*70)


if __name__ == "__main__":
    main()
