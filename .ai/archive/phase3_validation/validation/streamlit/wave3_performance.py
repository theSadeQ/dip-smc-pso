"""
Performance Measurement for Wave 3 Streamlit Theme Validation.

Measures:
1. CSS size (uncompressed and gzipped)
2. Load time impact (optional, requires running Streamlit)

Success Criteria:
- CSS <3KB gzipped
- Load time regression <50ms

Usage:
    python wave3_performance.py
"""
import gzip
import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.utils.streamlit_theme import load_design_tokens, generate_theme_css


def measure_css_size() -> dict:
    """Measure CSS size (uncompressed and gzipped)."""
    print("Loading design tokens...")
    tokens = load_design_tokens()

    print("Generating CSS...")
    css = generate_theme_css(tokens)

    # Get sizes
    uncompressed_bytes = len(css.encode('utf-8'))
    gzipped_bytes = len(gzip.compress(css.encode('utf-8')))

    # Calculate compression ratio
    compression_ratio = uncompressed_bytes / gzipped_bytes if gzipped_bytes > 0 else 0

    results = {
        "uncompressed_bytes": uncompressed_bytes,
        "uncompressed_kb": round(uncompressed_bytes / 1024, 2),
        "gzipped_bytes": gzipped_bytes,
        "gzipped_kb": round(gzipped_bytes / 1024, 2),
        "compression_ratio": round(compression_ratio, 2),
        "target_gzipped_bytes": 3072,  # 3KB
        "meets_target": gzipped_bytes < 3072
    }

    return results


def generate_report(css_results: dict) -> None:
    """Generate performance report."""
    script_dir = Path(__file__).parent
    output_dir = script_dir / "wave3"
    output_dir.mkdir(exist_ok=True)

    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "wave": "Wave 3 - Streamlit Theme Parity"
        },
        "css_size": css_results,
        "assessment": {
            "css_size_pass": css_results["meets_target"],
            "overall_pass": css_results["meets_target"]
        }
    }

    # Save JSON report
    json_path = output_dir / "performance_metrics.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n[REPORT] JSON saved: {json_path}")

    # Generate Markdown summary
    md_path = output_dir / "performance_summary.md"
    with open(md_path, 'w') as f:
        f.write("# Wave 3 Performance Measurement\n\n")
        f.write(f"**Date**: {results['metadata']['timestamp']}\n\n")

        # CSS Size Metrics
        f.write("## CSS Size Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Uncompressed | {css_results['uncompressed_bytes']} bytes ({css_results['uncompressed_kb']} KB) |\n")
        f.write(f"| **Gzipped** | **{css_results['gzipped_bytes']} bytes ({css_results['gzipped_kb']} KB)** |\n")
        f.write(f"| Compression Ratio | {css_results['compression_ratio']}x |\n")
        f.write(f"| Target (gzipped) | {css_results['target_gzipped_bytes']} bytes (3 KB) |\n")
        f.write(f"| **Status** | **{' PASS' if css_results['meets_target'] else ' FAIL'}** |\n\n")

        # Assessment
        f.write("## Assessment\n\n")
        if css_results["meets_target"]:
            f.write("[PASS] **PASS**: CSS size within budget (<3KB gzipped)\n\n")
            overhead_pct = (css_results['gzipped_bytes'] / css_results['target_gzipped_bytes']) * 100
            f.write(f"- Using {overhead_pct:.1f}% of 3KB budget\n")
            f.write(f"- Remaining budget: {css_results['target_gzipped_bytes'] - css_results['gzipped_bytes']} bytes\n")
        else:
            f.write("[FAIL] **FAIL**: CSS exceeds 3KB gzipped budget\n\n")
            overage = css_results['gzipped_bytes'] - css_results['target_gzipped_bytes']
            f.write(f"- Over budget by: {overage} bytes\n")
            f.write(f"- Recommend: Reduce CSS rules or optimize selectors\n")

        # Load Time (Manual)
        f.write("\n## Load Time Impact (Manual Test)\n\n")
        f.write("To measure load time impact:\n\n")
        f.write("1. **Baseline (theme disabled)**:\n")
        f.write("   - Set `config.yaml` → `streamlit.enable_dip_theme: false`\n")
        f.write("   - Restart Streamlit\n")
        f.write("   - Open DevTools (F12) → Performance tab\n")
        f.write("   - Record page load\n")
        f.write("   - Note \"Time to Interactive\" value\n\n")
        f.write("2. **Themed (theme enabled)**:\n")
        f.write("   - Set `config.yaml` → `streamlit.enable_dip_theme: true`\n")
        f.write("   - Restart Streamlit\n")
        f.write("   - Record page load again\n")
        f.write("   - Note \"Time to Interactive\" value\n\n")
        f.write("3. **Acceptance Criteria**:\n")
        f.write("   - Difference should be <50ms\n")
        f.write("   - CSS injection overhead should be negligible\n")

    print(f"[REPORT] Markdown saved: {md_path}")


def main():
    """Main execution."""
    print(f"{'='*60}")
    print(f"Wave 3 Performance Measurement")
    print(f"{'='*60}\n")

    try:
        print("[1/1] Measuring CSS size...")
        css_results = measure_css_size()

        print(f"\n[OK] CSS Size Measured:")
        print(f"  Uncompressed: {css_results['uncompressed_bytes']} bytes ({css_results['uncompressed_kb']} KB)")
        print(f"  Gzipped:      {css_results['gzipped_bytes']} bytes ({css_results['gzipped_kb']} KB)")
        print(f"  Compression:  {css_results['compression_ratio']}x")
        print(f"  Target:       {css_results['target_gzipped_bytes']} bytes (3 KB)")
        print(f"  Status:       {'PASS ✓' if css_results['meets_target'] else 'FAIL ✗'}")

        generate_report(css_results)

        print(f"\n{'='*60}")
        print("PERFORMANCE MEASUREMENT COMPLETE")
        print(f"{'='*60}")

        if css_results["meets_target"]:
            print("[PASS] CSS size validation PASSED")
        else:
            print("[FAIL] CSS size validation FAILED")
            exit(1)

    except FileNotFoundError as e:
        print(f"\n[ERROR] Design tokens not found: {e}")
        print("Ensure .codex/phase2_audit/design_tokens_v2.json exists")
        exit(1)
    except Exception as e:
        print(f"\n[ERROR] Performance measurement failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
