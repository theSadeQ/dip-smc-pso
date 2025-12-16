"""Quick baseline cost test to establish realistic targets.

Tests baseline gains from config.yaml with current cost function to determine
what "good" costs look like with new weights (state_error=1.0).
"""
import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.robust_cost_evaluator import RobustCostEvaluator


def test_baseline_costs():
    """Evaluate baseline and optimized gains with current cost function."""
    config = load_config("config.yaml")

    # Test configurations
    controllers = [
        ('sta_smc', 6),
        ('adaptive_smc', 5),
        ('hybrid_adaptive_sta_smc', 4)
    ]

    print("=" * 80)
    print("BASELINE COST EVALUATION - Current Cost Function (state_error=1.0)")
    print("=" * 80)
    print()

    for ctrl_name, n_gains in controllers:
        print(f"[{ctrl_name}]")

        # Get baseline gains
        baseline_gains = config.controller_defaults[ctrl_name].gains
        print(f"  Baseline gains: {baseline_gains}")

        # Get optimized gains (from MT-8 if available)
        optimized_gains = config.controllers[ctrl_name].gains
        print(f"  Optimized gains: {optimized_gains}")

        # Create cost evaluator with 5 scenarios (matching current run)
        def controller_factory(gains):
            return create_controller(ctrl_name, config, gains=gains)

        evaluator = RobustCostEvaluator(
            controller_factory=controller_factory,
            config=config,
            seed=42,
            n_scenarios=5,  # Match current run
            worst_case_weight=0.3
        )

        # Evaluate baseline
        print(f"  Evaluating baseline...")
        baseline_cost = evaluator.evaluate_single_robust(np.array(baseline_gains))
        print(f"  Baseline cost: {baseline_cost:.4f}")

        # Evaluate optimized
        print(f"  Evaluating optimized...")
        optimized_cost = evaluator.evaluate_single_robust(np.array(optimized_gains))
        print(f"  Optimized cost: {optimized_cost:.4f}")

        improvement = ((baseline_cost - optimized_cost) / baseline_cost) * 100
        print(f"  Improvement: {improvement:.2f}%")
        print()

    print("=" * 80)
    print("INTERPRETATION:")
    print("  - Baseline costs show what untrained controllers achieve")
    print("  - Optimized costs show what MT-8 gains achieve with NEW weights")
    print("  - Target for PSO: Beat optimized cost (or get close)")
    print("=" * 80)


if __name__ == "__main__":
    test_baseline_costs()
