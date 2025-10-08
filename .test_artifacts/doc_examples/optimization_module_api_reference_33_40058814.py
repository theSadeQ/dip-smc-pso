# Example from: docs\api\optimization_module_api_reference.md
# Index: 33
# Runnable: False
# Hash: 40058814

#!/usr/bin/env python3
"""
Example 3: Bounds Validation and Automatic Adjustment

Demonstrates:
- PSOBoundsValidator usage
- Controller-specific bounds validation
- Automatic adjustment algorithms
- Performance comparison with/without adjustment
"""

from src.optimization.validation.pso_bounds_validator import PSOBoundsValidator
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import create_controller
from src.config import load_config
from functools import partial
import numpy as np

# ============================================================================
# Configuration
# ============================================================================

CONFIG_PATH = "config.yaml"
CONTROLLER_TYPE = 'adaptive_smc'

# Test bounds (intentionally suboptimal)
TEST_BOUNDS_LOWER = [0.1, 0.1, 0.1, 0.1, 0.01]  # Too narrow
TEST_BOUNDS_UPPER = [5.0, 5.0, 5.0, 5.0, 1.0]   # Too narrow

# ============================================================================
# Main
# ============================================================================

def main():
    # Load configuration
    config = load_config(CONFIG_PATH)

    # Initialize bounds validator
    validator = PSOBoundsValidator(config)

    # Validate test bounds
    print("Validating test bounds for Adaptive SMC...")
    print(f"Lower: {TEST_BOUNDS_LOWER}")
    print(f"Upper: {TEST_BOUNDS_UPPER}")
    print()

    result = validator.validate_bounds(
        controller_type=CONTROLLER_TYPE,
        lower_bounds=TEST_BOUNDS_LOWER,
        upper_bounds=TEST_BOUNDS_UPPER
    )

    if result.is_valid:
        print("✓ Bounds are valid!")
    else:
        print("✗ Bounds validation failed!")
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

        print("\nRecommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")

        if result.adjusted_bounds:
            print("\nAutomatically adjusted bounds:")
            adjusted_lower = result.adjusted_bounds['lower']
            adjusted_upper = result.adjusted_bounds['upper']
            print(f"  Lower: {adjusted_lower}")
            print(f"  Upper: {adjusted_upper}")

            # Compare PSO performance with original vs. adjusted bounds
            print("\n" + "="*80)
            print("Performance Comparison: Original vs. Adjusted Bounds")
            print("="*80)

            controller_factory = partial(
                create_controller,
                controller_type=CONTROLLER_TYPE,
                config=config
            )

            # PSO with original bounds
            print("\n[1/2] Running PSO with ORIGINAL bounds...")
            tuner_original = PSOTuner(
                controller_factory=controller_factory,
                config=config,
                seed=42
            )
            # Override bounds
            config.pso.bounds.min = TEST_BOUNDS_LOWER
            config.pso.bounds.max = TEST_BOUNDS_UPPER
            result_original = tuner_original.optimise(iters_override=50)

            # PSO with adjusted bounds
            print("[2/2] Running PSO with ADJUSTED bounds...")
            tuner_adjusted = PSOTuner(
                controller_factory=controller_factory,
                config=config,
                seed=42
            )
            # Override bounds with adjusted
            config.pso.bounds.min = adjusted_lower
            config.pso.bounds.max = adjusted_upper
            result_adjusted = tuner_adjusted.optimise(iters_override=50)

            # Compare results
            print("\n" + "="*80)
            print("Results Comparison")
            print("="*80)
            print(f"{'Metric':<30s} | {'Original Bounds':>20s} | {'Adjusted Bounds':>20s} | {'Improvement':>15s}")
            print("-"*80)

            cost_original = result_original['best_cost']
            cost_adjusted = result_adjusted['best_cost']
            improvement = (cost_original - cost_adjusted) / cost_original * 100

            print(f"{'Best Cost':<30s} | {cost_original:20.6f} | {cost_adjusted:20.6f} | {improvement:14.2f}%")
            print(f"{'Best Gains':<30s}")
            print(f"  Original: {result_original['best_pos']}")
            print(f"  Adjusted: {result_adjusted['best_pos']}")
            print("="*80)

            if improvement > 0:
                print(f"\n✓ Adjusted bounds achieved {improvement:.2f}% cost reduction!")
            else:
                print(f"\n✗ Adjusted bounds did not improve performance.")

if __name__ == "__main__":
    main()