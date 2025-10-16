"""
Visual Regression Analysis for Wave 3 Streamlit Theme Validation.

Compares baseline (no theme) vs themed screenshots to detect visual changes.
Generates pixel difference analysis and change percentage metrics.

Usage:
    python wave3_visual_regression.py
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from PIL import Image, ImageChops, ImageStat
    import numpy as np
except ImportError:
    print("[ERROR] Required packages not installed")
    print("Install with: pip install Pillow numpy")
    exit(1)


def calculate_pixel_difference(img1: Image.Image, img2: Image.Image) -> Tuple[float, Image.Image]:
    """
    Calculate pixel-wise difference between two images.

    Returns:
        (difference_percentage, diff_image)
    """
    # Ensure same size
    if img1.size != img2.size:
        raise ValueError(f"Image size mismatch: {img1.size} vs {img2.size}")

    # Convert to RGB if needed
    if img1.mode != 'RGB':
        img1 = img1.convert('RGB')
    if img2.mode != 'RGB':
        img2 = img2.convert('RGB')

    # Calculate difference
    diff = ImageChops.difference(img1, img2)

    # Get statistics
    stat = ImageStat.Stat(diff)
    sum_of_squares = sum((value / 255.0) ** 2 for value in stat.sum)
    rms = (sum_of_squares / len(stat.sum)) ** 0.5

    # Convert to percentage (0-100)
    difference_percentage = rms * 100

    return difference_percentage, diff


def analyze_image_pair(baseline_path: Path, themed_path: Path) -> Dict:
    """Analyze a single image pair."""
    result = {
        "baseline": baseline_path.name,
        "themed": themed_path.name,
        "status": "success",
    }

    try:
        # Load images
        baseline_img = Image.open(baseline_path)
        themed_img = Image.open(themed_path)

        # Calculate difference
        diff_pct, diff_img = calculate_pixel_difference(baseline_img, themed_img)

        result["difference_percentage"] = round(diff_pct, 2)
        result["dimensions"] = {
            "baseline": baseline_img.size,
            "themed": themed_img.size
        }

        # Assess change magnitude
        if diff_pct < 5:
            result["assessment"] = "MINIMAL" # Very small changes
        elif diff_pct < 20:
            result["assessment"] = "MODERATE"  # Expected theme changes
        elif diff_pct < 50:
            result["assessment"] = "SIGNIFICANT"  # Large but acceptable
        else:
            result["assessment"] = "EXTREME"  # Possibly broken

        # Save difference image
        diff_output_dir = baseline_path.parent.parent / "diffs"
        diff_output_dir.mkdir(exist_ok=True)
        diff_output_path = diff_output_dir / f"diff_{baseline_path.name}"
        diff_img.save(diff_output_path)
        result["diff_image"] = str(diff_output_path.name)

    except FileNotFoundError as e:
        result["status"] = "error"
        result["error"] = f"File not found: {e}"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def run_visual_regression() -> Dict:
    """Run complete visual regression analysis."""
    script_dir = Path(__file__).parent
    baseline_dir = script_dir / "wave3" / "baseline"
    themed_dir = script_dir / "wave3" / "themed"

    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "baseline_dir": str(baseline_dir),
            "themed_dir": str(themed_dir),
        },
        "comparisons": [],
        "summary": {
            "total_comparisons": 0,
            "successful": 0,
            "errors": 0,
            "minimal_changes": 0,
            "moderate_changes": 0,
            "significant_changes": 0,
            "extreme_changes": 0,
        }
    }

    # Check directories exist
    if not baseline_dir.exists():
        print(f"[ERROR] Baseline directory not found: {baseline_dir}")
        print("Run: python wave3_screenshot_capture.py baseline")
        return results

    if not themed_dir.exists():
        print(f"[ERROR] Themed directory not found: {themed_dir}")
        print("Run: python wave3_screenshot_capture.py themed")
        return results

    # Find matching image pairs
    baseline_images = sorted(baseline_dir.glob("*.png"))

    print(f"{'='*60}")
    print(f"Visual Regression Analysis")
    print(f"{'='*60}")
    print(f"Baseline: {baseline_dir}")
    print(f"Themed: {themed_dir}")
    print(f"Images to compare: {len(baseline_images)}\n")

    for baseline_path in baseline_images:
        themed_path = themed_dir / baseline_path.name

        print(f"Comparing: {baseline_path.name}...", end=" ")

        if not themed_path.exists():
            print(f"[SKIP] Themed version not found")
            result = {
                "baseline": baseline_path.name,
                "status": "error",
                "error": "Themed version not found"
            }
        else:
            result = analyze_image_pair(baseline_path, themed_path)

            if result["status"] == "success":
                diff_pct = result["difference_percentage"]
                assessment = result["assessment"]
                print(f"[{assessment}] {diff_pct}% difference")

                # Update summary counts
                results["summary"]["successful"] += 1
                if assessment == "MINIMAL":
                    results["summary"]["minimal_changes"] += 1
                elif assessment == "MODERATE":
                    results["summary"]["moderate_changes"] += 1
                elif assessment == "SIGNIFICANT":
                    results["summary"]["significant_changes"] += 1
                elif assessment == "EXTREME":
                    results["summary"]["extreme_changes"] += 1
            else:
                print(f"[ERROR] {result.get('error', 'Unknown error')}")
                results["summary"]["errors"] += 1

        results["comparisons"].append(result)
        results["summary"]["total_comparisons"] += 1

    return results


def generate_report(results: Dict) -> None:
    """Generate JSON and Markdown reports."""
    script_dir = Path(__file__).parent
    output_dir = script_dir / "wave3"

    # Save JSON report
    json_path = output_dir / "visual_regression_report.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n[REPORT] JSON saved: {json_path}")

    # Generate Markdown summary
    md_path = output_dir / "visual_regression_summary.md"
    with open(md_path, 'w') as f:
        f.write("# Wave 3 Visual Regression Analysis\n\n")
        f.write(f"**Date**: {results['metadata']['timestamp']}\n\n")

        # Summary table
        f.write("## Summary\n\n")
        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total Comparisons | {results['summary']['total_comparisons']} |\n")
        f.write(f"| Successful | {results['summary']['successful']} |\n")
        f.write(f"| Errors | {results['summary']['errors']} |\n")
        f.write(f"| Minimal Changes (<5%) | {results['summary']['minimal_changes']} |\n")
        f.write(f"| Moderate Changes (5-20%) | {results['summary']['moderate_changes']} |\n")
        f.write(f"| Significant Changes (20-50%) | {results['summary']['significant_changes']} |\n")
        f.write(f"| **Extreme Changes (>50%)** | **{results['summary']['extreme_changes']}** |\n\n")

        # Assessment
        f.write("## Assessment\n\n")
        if results['summary']['extreme_changes'] > 0:
            f.write("[FAIL] **FAIL**: Extreme changes detected (>50% pixel difference)\n")
            f.write("- Review affected screenshots for layout breaks or missing widgets\n\n")
        elif results['summary']['significant_changes'] > 3:
            f.write("[WARN] **WARNING**: Multiple significant changes detected\n")
            f.write("- Expected for theme changes, but verify visual correctness\n\n")
        else:
            f.write("[PASS] **PASS**: Visual changes within expected range\n")
            f.write("- Theme applied successfully without layout issues\n\n")

        # Detailed results
        f.write("## Detailed Results\n\n")
        for comparison in results["comparisons"]:
            if comparison["status"] == "success":
                name = comparison["baseline"]
                diff = comparison["difference_percentage"]
                assessment = comparison["assessment"]
                icon = {
                    "MINIMAL": "[OK]",
                    "MODERATE": "[OK]",
                    "SIGNIFICANT": "[WARN]",
                    "EXTREME": "[FAIL]"
                }.get(assessment, "[?]")

                f.write(f"### {icon} {name}\n\n")
                f.write(f"- **Difference**: {diff}%\n")
                f.write(f"- **Assessment**: {assessment}\n")
                f.write(f"- **Diff Image**: `diffs/{comparison['diff_image']}`\n\n")
            else:
                f.write(f"### [ERROR] {comparison['baseline']}\n\n")
                f.write(f"- **Error**: {comparison.get('error', 'Unknown')}\n\n")

    print(f"[REPORT] Markdown saved: {md_path}")


def main():
    """Main execution."""
    print("Starting Visual Regression Analysis...\n")

    results = run_visual_regression()

    if results["summary"]["total_comparisons"] == 0:
        print("\n[ERROR] No comparisons performed")
        print("Ensure both baseline and themed screenshots exist")
        return

    generate_report(results)

    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total comparisons: {results['summary']['total_comparisons']}")
    print(f"Successful: {results['summary']['successful']}")
    print(f"Errors: {results['summary']['errors']}")
    print(f"\nChange Distribution:")
    print(f"  Minimal (<5%):       {results['summary']['minimal_changes']}")
    print(f"  Moderate (5-20%):    {results['summary']['moderate_changes']}")
    print(f"  Significant (20-50%): {results['summary']['significant_changes']}")
    print(f"  Extreme (>50%):      {results['summary']['extreme_changes']}")

    if results['summary']['extreme_changes'] > 0:
        print(f"\n[FAIL] Validation FAILED: Extreme changes detected")
        exit(1)
    else:
        print(f"\n[PASS] Validation PASSED: Changes within acceptable range")


if __name__ == "__main__":
    main()
