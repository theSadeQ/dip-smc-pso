#======================================================================================\
#================= scripts/diagnostic/test_scenario_difficulty.py ==================\
#======================================================================================\
"""
Phase 1.2: Scenario Difficulty Validation

Tests whether scenario configuration is reasonable or too challenging:
1. MT-8 gains on each of current 5 scenarios individually
2. 5-scenario vs 10-scenario comparison (cost ratio should be <1.5x)
3. 5s vs 7s duration comparison (ranking correlation should be >0.9)

Usage:
    python scripts/diagnostic/test_scenario_difficulty.py

Expected Results:
    [OK] MT-8 stable on >=4/5 current scenarios
    [OK] 5-scenario robust cost <20
    [OK] Duration doesn't change ranking

Author: Claude Code
Date: December 2025
"""

import numpy as np
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from scipy.stats import spearmanr

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.robust_cost_evaluator import RobustCostEvaluator


# MT-8 Optimized Gains
MT8_GAINS = {
    'sta_smc': np.array([2.02, 6.67, 5.62, 3.75, 4.36, 2.05]),
    'adaptive_smc': np.array([2.14, 3.36, 7.20, 0.34, 0.29]),
    'classical_smc': np.array([23.07, 12.85, 5.51, 3.49, 2.23, 0.15]),
    'hybrid_adaptive_sta_smc': np.array([10.15, 12.84, 6.82, 2.75])
}


def create_controller_factory(controller_type: str, config):
    """Create controller factory function."""
    def factory(gains):
        controller_config = getattr(config.controllers, controller_type)
        config_dict = (controller_config.model_dump()
                      if hasattr(controller_config, 'model_dump')
                      else dict(controller_config))
        config_dict['max_force'] = 150.0
        return create_controller(controller_type, config=config_dict, gains=gains)
    return factory


def test_mt8_individual_scenarios(controller_type: str = 'sta_smc') -> Dict:
    """Test 1: MT-8 gains on each scenario individually.

    Expected: >=4/5 scenarios stable (cost <100), mean <25, worst <100
    If <3/5 stable: scenarios too hard!
    """
    print("\n" + "="*80)
    print("TEST 1: MT-8 Gains on Individual Scenarios")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)
    mt8_gains = MT8_GAINS[controller_type]

    # Create evaluator with CURRENT Phase 2.3 settings
    evaluator = RobustCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0,
        n_scenarios=5,
        worst_case_weight=0.3,
        scenario_distribution={
            'nominal': 0.4,
            'moderate': 0.4,
            'large': 0.2
        },
        nominal_range=0.05,
        moderate_range=0.15,
        large_range=0.25
    )

    print(f"\nTesting {controller_type} with MT-8 gains: {mt8_gains}")
    print(f"Scenarios: {len(evaluator.scenarios)}")

    # Test each scenario individually
    costs = []
    stable_count = 0

    for i, scenario in enumerate(evaluator.scenarios):
        # Create single-scenario evaluator
        single_evaluator = RobustCostEvaluator(
            controller_factory=factory,
            config=config,
            seed=42 + i,
            u_max=150.0,
            n_scenarios=1,
            worst_case_weight=0.0,  # No worst-case penalty for single scenario
            scenario_distribution={'nominal': 1.0, 'moderate': 0.0, 'large': 0.0},
            nominal_range=0.0,  # Use exact scenario
            moderate_range=0.0,
            large_range=0.0
        )
        # Override scenario
        single_evaluator.scenarios = [scenario]

        # Evaluate
        cost = single_evaluator.evaluate_single_robust(mt8_gains)
        costs.append(cost)

        stable = cost < 100.0
        if stable:
            stable_count += 1

        status = "[OK]" if stable else "[FAIL]"
        print(f"  Scenario {i+1}: {status} cost={cost:.2f}, IC={scenario[:3]}")

    mean_cost = np.mean(costs)
    worst_cost = np.max(costs)

    print(f"\n[INFO] Summary:")
    print(f"  Stable: {stable_count}/5 scenarios")
    print(f"  Mean cost: {mean_cost:.2f}")
    print(f"  Worst cost: {worst_cost:.2f}")

    # Validate
    if stable_count >= 4 and mean_cost < 25.0 and worst_cost < 100.0:
        print("[OK] Scenarios are reasonable difficulty")
        status = "PASS"
    elif stable_count >= 3:
        print(f"[WARNING] Marginal difficulty (stable {stable_count}/5)")
        status = "WARNING"
    else:
        print(f"[ERROR] Scenarios too hard! Only {stable_count}/5 stable")
        status = "FAIL"

    return {
        'test': 'MT-8 Individual Scenarios',
        'controller': controller_type,
        'stable_count': stable_count,
        'mean_cost': mean_cost,
        'worst_cost': worst_cost,
        'individual_costs': costs,
        'status': status
    }


def test_5_vs_10_scenarios(controller_type: str = 'sta_smc') -> Dict:
    """Test 2: 5-scenario vs 10-scenario comparison.

    Expected: 10-scenario cost <= 1.5x the 5-scenario cost
    If >2x: too many extreme scenarios
    """
    print("\n" + "="*80)
    print("TEST 2: 5-Scenario vs 10-Scenario Comparison")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)
    mt8_gains = MT8_GAINS[controller_type]

    print(f"\nTesting {controller_type} with MT-8 gains: {mt8_gains}")

    # Test 5-scenario (Phase 2.3 settings)
    evaluator_5 = RobustCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0,
        n_scenarios=5,
        worst_case_weight=0.3,
        scenario_distribution={
            'nominal': 0.4,
            'moderate': 0.4,
            'large': 0.2
        },
        nominal_range=0.05,
        moderate_range=0.15,
        large_range=0.25
    )
    cost_5 = evaluator_5.evaluate_single_robust(mt8_gains)
    print(f"\n[INFO] 5-scenario cost: {cost_5:.4f}")

    # Test 10-scenario (OLD settings)
    evaluator_10 = RobustCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0,
        n_scenarios=10,
        worst_case_weight=0.3,
        scenario_distribution={
            'nominal': 0.2,
            'moderate': 0.3,
            'large': 0.5
        },
        nominal_range=0.05,
        moderate_range=0.15,
        large_range=0.3
    )
    cost_10 = evaluator_10.evaluate_single_robust(mt8_gains)
    print(f"[INFO] 10-scenario cost: {cost_10:.4f}")

    # Calculate ratio
    ratio = cost_10 / cost_5 if cost_5 > 0 else float('inf')
    print(f"\n[INFO] Cost ratio (10/5): {ratio:.2f}x")

    # Validate
    if ratio < 1.5:
        print("[OK] 10-scenario cost reasonable (<1.5x)")
        status = "PASS"
    elif ratio < 2.0:
        print(f"[WARNING] 10-scenario cost elevated ({ratio:.2f}x)")
        status = "WARNING"
    else:
        print(f"[ERROR] 10-scenario cost too high! {ratio:.2f}x > 2.0x")
        status = "FAIL"

    return {
        'test': '5 vs 10 Scenarios',
        'controller': controller_type,
        'cost_5': cost_5,
        'cost_10': cost_10,
        'ratio': ratio,
        'status': status
    }


def test_duration_sensitivity(controller_type: str = 'sta_smc', n_samples: int = 10) -> Dict:
    """Test 3: 5s vs 7s duration comparison.

    Expected: Rank correlation >0.9 (same ranking)
    If <0.7: duration changes optimization landscape
    """
    print("\n" + "="*80)
    print("TEST 3: Duration Sensitivity (5s vs 7s)")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Generate random gain sets for testing
    bounds_config = config.pso.bounds
    controller_bounds = getattr(bounds_config, controller_type)
    min_bounds = np.array(controller_bounds.min)
    max_bounds = np.array(controller_bounds.max)

    rng = np.random.default_rng(42)
    random_gains = [
        min_bounds + rng.random(len(min_bounds)) * (max_bounds - min_bounds)
        for _ in range(n_samples)
    ]

    print(f"\nTesting {n_samples} random gain sets")

    # Create evaluators with different durations
    # Temporarily override duration in config
    original_duration = config.simulation.duration

    # Test with 5s duration
    config.simulation.duration = 5.0
    evaluator_5s = RobustCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0,
        n_scenarios=5,
        worst_case_weight=0.3,
        scenario_distribution={'nominal': 0.4, 'moderate': 0.4, 'large': 0.2},
        nominal_range=0.05,
        moderate_range=0.15,
        large_range=0.25
    )

    costs_5s = []
    for i, gains in enumerate(random_gains):
        try:
            cost = evaluator_5s.evaluate_single_robust(gains)
            costs_5s.append(cost)
            print(f"  Sample {i+1}/10: 5s cost={cost:.2f}", end='\r')
        except Exception as e:
            costs_5s.append(1000.0)  # Penalty for failures
    print()

    # Test with 7s duration
    config.simulation.duration = 7.0
    evaluator_7s = RobustCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0,
        n_scenarios=5,
        worst_case_weight=0.3,
        scenario_distribution={'nominal': 0.4, 'moderate': 0.4, 'large': 0.2},
        nominal_range=0.05,
        moderate_range=0.15,
        large_range=0.25
    )

    costs_7s = []
    for i, gains in enumerate(random_gains):
        try:
            cost = evaluator_7s.evaluate_single_robust(gains)
            costs_7s.append(cost)
            print(f"  Sample {i+1}/10: 7s cost={cost:.2f}", end='\r')
        except Exception as e:
            costs_7s.append(1000.0)
    print()

    # Restore original duration
    config.simulation.duration = original_duration

    # Calculate correlation
    correlation, p_value = spearmanr(costs_5s, costs_7s)

    print(f"\n[INFO] Spearman correlation: {correlation:.3f} (p={p_value:.4f})")

    # Validate
    if correlation > 0.9:
        print("[OK] Duration doesn't affect ranking (correlation >0.9)")
        status = "PASS"
    elif correlation > 0.7:
        print(f"[WARNING] Moderate duration effect (correlation {correlation:.3f})")
        status = "WARNING"
    else:
        print(f"[ERROR] Duration significantly changes ranking! Correlation {correlation:.3f}")
        status = "FAIL"

    return {
        'test': 'Duration Sensitivity',
        'controller': controller_type,
        'correlation': correlation,
        'p_value': p_value,
        'costs_5s': costs_5s,
        'costs_7s': costs_7s,
        'status': status
    }


def main():
    """Run all Phase 1.2 diagnostic tests."""
    print("\n" + "#"*80)
    print("# PHASE 1.2: SCENARIO DIFFICULTY VALIDATION")
    print("#"*80)

    controller_type = 'sta_smc'

    # Run all tests
    results = []
    results.append(test_mt8_individual_scenarios(controller_type))
    results.append(test_5_vs_10_scenarios(controller_type))
    results.append(test_duration_sensitivity(controller_type))

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    for result in results:
        status_symbol = {
            'PASS': '[OK]',
            'WARNING': '[WARNING]',
            'FAIL': '[ERROR]'
        }[result['status']]
        print(f"{status_symbol} {result['test']}: {result['status']}")

    # Overall verdict
    passed = sum(1 for r in results if r['status'] == 'PASS')
    warnings = sum(1 for r in results if r['status'] == 'WARNING')
    failed = sum(1 for r in results if r['status'] == 'FAIL')

    print(f"\n[INFO] Results: {passed} PASS, {warnings} WARNING, {failed} FAIL")

    if failed == 0 and warnings == 0:
        print("\n[OK] All tests passed! Scenario difficulty is appropriate.")
        print("[INFO] Phase 2.3 scenario reduction validated.")
    elif failed == 0:
        print("\n[WARNING] All tests passed with warnings. Scenarios acceptable but monitor.")
    else:
        print("\n[ERROR] Critical failures! Scenarios may be too challenging.")
        print("[INFO] Consider further reducing:")
        for result in results:
            if result['status'] == 'FAIL':
                print(f"  - {result['test']}")

    return results


if __name__ == "__main__":
    main()
