#======================================================================================\
#================= scripts/diagnostic/test_warmstart_quality.py ====================\
#======================================================================================\
"""
Phase 1.3: Baseline Warm-Start Quality Tests

Tests whether MT-8 gains provide good PSO warm-start:
1. MT-8 vs config baseline quality (MT-8 should be better)
2. MT-8 baseline vs 100 random samples (should be top 20%)
3. Initial swarm quality (>=5 particles with cost <50)

Usage:
    python scripts/diagnostic/test_warmstart_quality.py

Expected Results:
    [OK] MT-8 cost <30
    [OK] MT-8 beats >80% of random samples
    [OK] Initial swarm has >=5 good particles

Author: Claude Code
Date: December 2025
"""

import numpy as np
import sys
from pathlib import Path
from typing import Dict, List

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


def test_mt8_vs_baseline_quality(controller_type: str = 'sta_smc') -> Dict:
    """Test 1: MT-8 vs config baseline quality.

    Expected: MT-8 cost <30, better than config baseline
    """
    print("\n" + "="*80)
    print("TEST 1: MT-8 vs Config Baseline Quality")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create evaluator with Phase 2.3 settings
    evaluator = RobustCostEvaluator(
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

    # Test MT-8 gains
    mt8_gains = MT8_GAINS[controller_type]
    mt8_cost = evaluator.evaluate_single_robust(mt8_gains)
    print(f"\n[INFO] MT-8 gains: {mt8_gains}")
    print(f"[INFO] MT-8 cost: {mt8_cost:.4f}")

    # Test config baseline gains
    try:
        baseline_config = getattr(config.controller_defaults, controller_type)
        baseline_gains = np.array(baseline_config.gains[:len(mt8_gains)])
        baseline_cost = evaluator.evaluate_single_robust(baseline_gains)
        print(f"\n[INFO] Config baseline gains: {baseline_gains}")
        print(f"[INFO] Config baseline cost: {baseline_cost:.4f}")
    except Exception as e:
        print(f"\n[WARNING] Could not load config baseline: {e}")
        baseline_cost = None

    # Validate
    mt8_pass = mt8_cost < 30.0
    better_than_baseline = (baseline_cost is None or mt8_cost < baseline_cost)

    if mt8_pass and better_than_baseline:
        print("\n[OK] MT-8 gains provide excellent warm-start")
        status = "PASS"
    elif mt8_pass:
        print(f"\n[WARNING] MT-8 cost acceptable but not better than baseline")
        status = "WARNING"
    else:
        print(f"\n[ERROR] MT-8 cost too high ({mt8_cost:.2f} >= 30.0)")
        status = "FAIL"

    return {
        'test': 'MT-8 vs Baseline Quality',
        'controller': controller_type,
        'mt8_cost': mt8_cost,
        'baseline_cost': baseline_cost,
        'status': status
    }


def test_mt8_vs_random_samples(controller_type: str = 'sta_smc', n_samples: int = 100) -> Dict:
    """Test 2: MT-8 baseline vs random samples.

    Expected: MT-8 beats >80% of random samples (top 20%)
    """
    print("\n" + "="*80)
    print("TEST 2: MT-8 vs Random Samples")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create evaluator
    evaluator = RobustCostEvaluator(
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

    # Get bounds
    bounds_config = config.pso.bounds
    controller_bounds = getattr(bounds_config, controller_type)
    min_bounds = np.array(controller_bounds.min)
    max_bounds = np.array(controller_bounds.max)

    # Test MT-8 gains
    mt8_gains = MT8_GAINS[controller_type]
    mt8_cost = evaluator.evaluate_single_robust(mt8_gains)

    print(f"\nTesting MT-8 vs {n_samples} random samples")
    print(f"[INFO] MT-8 cost: {mt8_cost:.4f}")

    # Generate and test random samples
    rng = np.random.default_rng(42)
    random_costs = []

    for i in range(n_samples):
        random_gains = min_bounds + rng.random(len(min_bounds)) * (max_bounds - min_bounds)
        try:
            cost = evaluator.evaluate_single_robust(random_gains)
            random_costs.append(cost)
        except Exception:
            random_costs.append(1000.0)  # Penalty for failures

        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{n_samples} samples", end='\r')

    print(f"\n\n[INFO] Random samples:")
    print(f"  Mean: {np.mean(random_costs):.2f}")
    print(f"  Std: {np.std(random_costs):.2f}")
    print(f"  Min: {np.min(random_costs):.2f}")
    print(f"  Max: {np.max(random_costs):.2f}")

    # Calculate MT-8 rank
    better_count = sum(1 for cost in random_costs if mt8_cost < cost)
    percentile = (better_count / n_samples) * 100

    print(f"\n[INFO] MT-8 beats {better_count}/{n_samples} random samples ({percentile:.1f}%)")

    # Validate
    if percentile >= 80.0:
        print("[OK] MT-8 in top 20% (beats >=80% of random)")
        status = "PASS"
    elif percentile >= 60.0:
        print(f"[WARNING] MT-8 in top 40% (beats {percentile:.1f}%)")
        status = "WARNING"
    else:
        print(f"[ERROR] MT-8 not competitive (only beats {percentile:.1f}%)")
        status = "FAIL"

    return {
        'test': 'MT-8 vs Random Samples',
        'controller': controller_type,
        'mt8_cost': mt8_cost,
        'percentile': percentile,
        'random_mean': np.mean(random_costs),
        'random_std': np.std(random_costs),
        'status': status
    }


def test_initial_swarm_quality(controller_type: str = 'sta_smc', n_particles: int = 25) -> Dict:
    """Test 3: Initial swarm quality.

    Expected: >=5 particles with cost <50 (warm-start working)
    """
    print("\n" + "="*80)
    print("TEST 3: Initial Swarm Quality")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create evaluator
    evaluator = RobustCostEvaluator(
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

    # Get bounds
    bounds_config = config.pso.bounds
    controller_bounds = getattr(bounds_config, controller_type)
    min_bounds = np.array(controller_bounds.min)
    max_bounds = np.array(controller_bounds.max)

    # Generate warm-start swarm (50% MT-8 + 50% random, matching Phase 2.4)
    mt8_gains = MT8_GAINS[controller_type]
    rng = np.random.default_rng(42)

    n_baseline = int(0.50 * n_particles)  # Phase 2.4: 50% near MT-8
    n_random = n_particles - n_baseline

    print(f"\nGenerating {n_particles} particle swarm:")
    print(f"  {n_baseline} particles near MT-8 gains")
    print(f"  {n_random} particles random exploration")

    # Generate particles
    swarm = []
    noise_std = 0.1 * (max_bounds - min_bounds)

    # MT-8-based particles
    for i in range(n_baseline):
        noisy_gains = mt8_gains + rng.normal(0, noise_std)
        noisy_gains = np.clip(noisy_gains, min_bounds, max_bounds)
        swarm.append(noisy_gains)

    # Random particles
    for i in range(n_random):
        random_gains = min_bounds + rng.random(len(min_bounds)) * (max_bounds - min_bounds)
        swarm.append(random_gains)

    # Evaluate swarm
    costs = []
    good_particles = 0

    for i, gains in enumerate(swarm):
        try:
            cost = evaluator.evaluate_single_robust(gains)
            costs.append(cost)
            if cost < 50.0:
                good_particles += 1
        except Exception:
            costs.append(1000.0)

        print(f"  Evaluating particle {i+1}/{n_particles}: cost={costs[-1]:.2f}", end='\r')

    print(f"\n\n[INFO] Initial swarm statistics:")
    print(f"  Best cost: {np.min(costs):.2f}")
    print(f"  Mean cost: {np.mean(costs):.2f}")
    print(f"  Worst cost: {np.max(costs):.2f}")
    print(f"  Good particles (<50): {good_particles}/{n_particles}")

    # Validate
    if good_particles >= 5:
        print(f"\n[OK] Initial swarm has {good_particles} good particles (>=5)")
        status = "PASS"
    elif good_particles >= 3:
        print(f"\n[WARNING] Only {good_particles} good particles (expected >=5)")
        status = "WARNING"
    else:
        print(f"\n[ERROR] Insufficient good particles ({good_particles} < 3)")
        status = "FAIL"

    return {
        'test': 'Initial Swarm Quality',
        'controller': controller_type,
        'n_particles': n_particles,
        'good_particles': good_particles,
        'best_cost': np.min(costs),
        'mean_cost': np.mean(costs),
        'worst_cost': np.max(costs),
        'status': status
    }


def main():
    """Run all Phase 1.3 diagnostic tests."""
    print("\n" + "#"*80)
    print("# PHASE 1.3: BASELINE WARM-START QUALITY TESTS")
    print("#"*80)

    controller_type = 'sta_smc'

    # Run all tests
    results = []
    results.append(test_mt8_vs_baseline_quality(controller_type))
    results.append(test_mt8_vs_random_samples(controller_type))
    results.append(test_initial_swarm_quality(controller_type))

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
        print("\n[OK] All tests passed! MT-8 warm-start validated.")
        print("[INFO] Phase 2.4 MT-8 baseline improvement confirmed.")
    elif failed == 0:
        print("\n[WARNING] Tests passed with warnings. Warm-start acceptable but monitor.")
    else:
        print("\n[ERROR] Critical failures! MT-8 baseline may not be optimal.")

    return results


if __name__ == "__main__":
    main()
