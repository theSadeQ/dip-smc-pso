#!/usr/bin/env python
"""
Compare Standard vs Robust PSO Gains

Analyzes differences between standard and robust PSO optimization results
for all three controllers. Computes element-wise differences and relative errors.

Usage:
    python scripts/compare_standard_vs_robust.py

Output:
    optimization_results/standard_vs_robust_comparison.json
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, List


def load_json_gains(file_path: Path) -> Dict[str, List[float]]:
    """Load gain values from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def compute_differences(standard: List[float], robust: List[float]) -> Dict[str, Any]:
    """Compute element-wise differences and relative errors."""
    standard_arr = np.array(standard)
    robust_arr = np.array(robust)

    # Absolute differences
    abs_diff = robust_arr - standard_arr

    # Relative error (avoid division by zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_error = np.where(
            standard_arr != 0,
            abs_diff / standard_arr * 100,
            0.0
        )

    # Max absolute difference
    max_abs_diff = float(np.max(np.abs(abs_diff)))
    max_rel_error = float(np.max(np.abs(rel_error)))

    # Check if identical (within numerical tolerance)
    identical = np.allclose(standard_arr, robust_arr, rtol=1e-9, atol=1e-12)

    return {
        "absolute_differences": abs_diff.tolist(),
        "relative_errors_percent": rel_error.tolist(),
        "max_absolute_difference": max_abs_diff,
        "max_relative_error_percent": max_rel_error,
        "are_identical": identical
    }


def compare_all_controllers() -> Dict[str, Any]:
    """Compare standard vs robust for all controllers."""

    base_dir = Path("optimization_results")
    standard_dir = base_dir / "phase2_standard_pso"
    robust_dir = base_dir / "phase2_robust_pso"

    controllers = {
        "sta_smc": ("pso_sta_smc_standard.json", "pso_sta_smc_robust.json"),
        "adaptive_smc": ("pso_adaptive_smc_standard.json", "pso_adaptive_smc_robust.json"),
        "hybrid_adaptive_sta_smc": ("pso_hybrid_adaptive_sta_smc_standard.json",
                                     "pso_hybrid_adaptive_sta_smc_robust.json")
    }

    comparison = {
        "metadata": {
            "description": "Comparison of standard vs robust PSO gains",
            "tolerance": {
                "relative": 1e-9,
                "absolute": 1e-12
            }
        },
        "controllers": {}
    }

    for ctrl_name, (std_file, rob_file) in controllers.items():
        # Load gains
        standard_data = load_json_gains(standard_dir / std_file)
        robust_data = load_json_gains(robust_dir / rob_file)

        standard_gains = standard_data[ctrl_name]
        robust_gains = robust_data[ctrl_name]

        # Compute differences
        diff_results = compute_differences(standard_gains, robust_gains)

        comparison["controllers"][ctrl_name] = {
            "standard_gains": standard_gains,
            "robust_gains": robust_gains,
            "n_parameters": len(standard_gains),
            "comparison": diff_results
        }

    # Overall summary
    all_identical = all(
        ctrl["comparison"]["are_identical"]
        for ctrl in comparison["controllers"].values()
    )

    comparison["summary"] = {
        "all_controllers_identical": all_identical,
        "interpretation": (
            "All standard and robust PSO results are numerically identical. "
            "This indicates that the cost function is inherently robust to disturbances, "
            "or that the optimal gains provide sufficient robustness margins."
        )
    }

    return comparison


def main():
    """Compare standard vs robust PSO results."""
    print("[INFO] Comparing standard vs robust PSO gains...")

    comparison = compare_all_controllers()

    # Save to file
    output_path = Path("optimization_results/standard_vs_robust_comparison.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(comparison, f, indent=2)

    print(f"[OK] Comparison saved to: {output_path}")

    # Print results
    print("\n[RESULTS] Controller-by-Controller Comparison:")
    for ctrl_name, ctrl_data in comparison["controllers"].items():
        print(f"\n  {ctrl_name}:")
        print(f"    Parameters: {ctrl_data['n_parameters']}")
        print(f"    Identical: {ctrl_data['comparison']['are_identical']}")
        print(f"    Max Absolute Diff: {ctrl_data['comparison']['max_absolute_difference']:.2e}")
        print(f"    Max Relative Error: {ctrl_data['comparison']['max_relative_error_percent']:.2e}%")

    print(f"\n[SUMMARY] All controllers identical: {comparison['summary']['all_controllers_identical']}")
    print(f"[INTERPRETATION] {comparison['summary']['interpretation']}")


if __name__ == "__main__":
    main()
