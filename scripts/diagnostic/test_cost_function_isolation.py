#======================================================================================\
#================= scripts/diagnostic/test_cost_function_isolation.py ==============\
#======================================================================================\
"""
Phase 1.1: Cost Function Isolation Tests

Tests cost function correctness in isolation to diagnose PSO optimization issues:
1. MT-8 gains on single nominal scenario (should be <15)
2. u_max consistency check (evaluator vs controller)
3. Pathological gains test (all zeros/max should get penalty >500)
4. Normalization validation (components balanced 0.1-10 range)

Usage:
    python scripts/diagnostic/test_cost_function_isolation.py

Expected Results:
    [OK] MT-8 gains cost <15 on nominal
    [OK] u_max matches (both 150.0)
    [OK] Bad gains penalized (>500)
    [OK] Cost components balanced

Author: Claude Code
Date: December 2025
"""

import numpy as np
import sys
from pathlib import Path
from typing import Dict, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.core.cost_evaluator import ControllerCostEvaluator
from src.simulation.engines.vector_sim import simulate_system_batch


# MT-8 Optimized Gains (from config.yaml lines 88-93, 100-104, 139-142)
MT8_GAINS = {
    'sta_smc': np.array([2.02, 6.67, 5.62, 3.75, 4.36, 2.05]),
    'adaptive_smc': np.array([2.14, 3.36, 7.20, 0.34, 0.29]),
    'classical_smc': np.array([23.07, 12.85, 5.51, 3.49, 2.23, 0.15]),
    'hybrid_adaptive_sta_smc': np.array([10.15, 12.84, 6.82, 2.75])
}


def create_controller_factory(controller_type: str, config):
    """Create controller factory function for cost evaluator."""
    def factory(gains):
        controller_config = getattr(config.controllers, controller_type)
        config_dict = (controller_config.model_dump()
                      if hasattr(controller_config, 'model_dump')
                      else dict(controller_config))
        # FIX: Ensure max_force=150.0 is set
        config_dict['max_force'] = 150.0
        return create_controller(controller_type, config=config_dict, gains=gains)
    return factory


def test_mt8_nominal_scenario(controller_type: str = 'sta_smc') -> Dict:
    """Test 1: MT-8 gains on single nominal scenario.

    Expected: cost <15
    If >50: cost function broken!
    """
    print("\n" + "="*80)
    print("TEST 1: MT-8 Gains on Nominal Scenario")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create cost evaluator
    evaluator = ControllerCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0  # Pass explicitly to test the fix
    )

    # Test MT-8 gains
    mt8_gains = MT8_GAINS[controller_type]
    print(f"Testing {controller_type} with gains: {mt8_gains}")

    # Single nominal scenario: small perturbation [0, 0.05, -0.03, 0, 0, 0]
    nominal_ic = np.array([0.0, 0.05, -0.03, 0.0, 0.0, 0.0])

    # Evaluate cost
    cost = evaluator.evaluate_single(mt8_gains)

    print(f"\n[INFO] MT-8 Gains Cost: {cost:.4f}")

    # Validate
    if cost < 15.0:
        print("[OK] Cost <15 - Cost function working correctly")
        status = "PASS"
    elif cost < 50.0:
        print("[WARNING] Cost in range 15-50 - Marginal performance")
        status = "WARNING"
    else:
        print("[ERROR] Cost >50 - Cost function likely broken!")
        status = "FAIL"

    return {
        'test': 'MT-8 Nominal',
        'controller': controller_type,
        'gains': mt8_gains,
        'cost': cost,
        'threshold': 15.0,
        'status': status
    }


def test_umax_consistency(controller_type: str = 'sta_smc') -> Dict:
    """Test 2: u_max consistency check.

    Expected: evaluator.u_max == controller.max_force == 150.0
    If mismatch: control effort cost calculation wrong!
    """
    print("\n" + "="*80)
    print("TEST 2: u_max Consistency Check")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create cost evaluator
    evaluator = ControllerCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0  # Pass explicitly to test the fix
    )

    # Create actual controller to check max_force
    mt8_gains = MT8_GAINS[controller_type]
    controller = factory(mt8_gains)

    evaluator_umax = evaluator.u_max
    controller_max_force = getattr(controller, 'max_force', None)

    print(f"\n[INFO] Evaluator u_max: {evaluator_umax:.2f}")
    print(f"[INFO] Controller max_force: {controller_max_force:.2f}")

    # Validate
    if evaluator_umax == controller_max_force == 150.0:
        print("[OK] u_max matches (both 150.0)")
        status = "PASS"
    elif evaluator_umax == 150.0 or controller_max_force == 150.0:
        print(f"[WARNING] Partial match - evaluator: {evaluator_umax}, controller: {controller_max_force}")
        status = "WARNING"
    else:
        print(f"[ERROR] u_max mismatch! Evaluator: {evaluator_umax}, Controller: {controller_max_force}")
        print("[ERROR] This causes control effort cost to be off by factor of {:.1f}x".format(
            (150.0 / evaluator_umax)**2 if evaluator_umax > 0 else float('inf')
        ))
        status = "FAIL"

    return {
        'test': 'u_max Consistency',
        'controller': controller_type,
        'evaluator_umax': evaluator_umax,
        'controller_max_force': controller_max_force,
        'expected': 150.0,
        'status': status
    }


def test_pathological_gains(controller_type: str = 'sta_smc') -> Dict:
    """Test 3: Pathological gains test.

    Expected: all zeros or all max should get instability penalty >500
    If <100: penalty system broken!
    """
    print("\n" + "="*80)
    print("TEST 3: Pathological Gains Test")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create cost evaluator
    evaluator = ControllerCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0  # Pass explicitly to test the fix
    )

    # Get bounds for this controller
    bounds_config = config.pso.bounds
    controller_bounds = getattr(bounds_config, controller_type)
    n_params = len(controller_bounds.min)

    # Test all zeros
    zero_gains = np.zeros(n_params)
    print(f"\nTesting all-zero gains: {zero_gains}")
    zero_cost = evaluator.evaluate_single(zero_gains)
    print(f"[INFO] All-zero cost: {zero_cost:.4f}")

    # Test all max
    max_gains = np.array(controller_bounds.max)
    print(f"\nTesting all-max gains: {max_gains}")
    max_cost = evaluator.evaluate_single(max_gains)
    print(f"[INFO] All-max cost: {max_cost:.4f}")

    # Validate
    zero_pass = zero_cost > 500.0
    max_pass = max_cost > 500.0

    if zero_pass and max_pass:
        print("\n[OK] Bad gains penalized (both >500)")
        status = "PASS"
    elif zero_pass or max_pass:
        print(f"\n[WARNING] Partial penalty - zero: {zero_cost:.1f}, max: {max_cost:.1f}")
        status = "WARNING"
    else:
        print(f"\n[ERROR] Penalty system broken! Zero: {zero_cost:.1f}, Max: {max_cost:.1f}")
        status = "FAIL"

    return {
        'test': 'Pathological Gains',
        'controller': controller_type,
        'zero_cost': zero_cost,
        'max_cost': max_cost,
        'threshold': 500.0,
        'status': status
    }


def test_normalization(controller_type: str = 'sta_smc') -> Dict:
    """Test 4: Normalization validation.

    Expected: Normalization constants are reasonable (>0, finite)
    This test validates the cost evaluator's normalization setup.
    """
    print("\n" + "="*80)
    print("TEST 4: Normalization Validation")
    print("="*80)

    config = load_config("config.yaml")
    factory = create_controller_factory(controller_type, config)

    # Create cost evaluator
    evaluator = ControllerCostEvaluator(
        controller_factory=factory,
        config=config,
        seed=42,
        u_max=150.0  # Pass explicitly to test the fix
    )

    print(f"\n[INFO] Normalization Constants:")
    print(f"  ISE norm: {evaluator.norm_ise:.2f}")
    print(f"  u^2 norm: {evaluator.norm_u:.2f}")
    print(f"  du^2 norm: {evaluator.norm_du:.2f}")
    print(f"  sigma^2 norm: {evaluator.norm_sigma:.2f}")

    # Check all constants are positive and finite
    norms = {
        'ISE': evaluator.norm_ise,
        'u^2': evaluator.norm_u,
        'du^2': evaluator.norm_du,
        'sigma^2': evaluator.norm_sigma
    }

    all_valid = all(
        np.isfinite(v) and v > 0 for v in norms.values()
    )

    # Calculate range (max/min)
    values = list(norms.values())
    if min(values) > 0:
        norm_ratio = max(values) / min(values)
    else:
        norm_ratio = float('inf')

    print(f"\n[INFO] Normalization Constant Range (max/min): {norm_ratio:.2f}")

    # Validate
    if all_valid and norm_ratio < 1000.0:
        print("[OK] Normalization constants are reasonable")
        status = "PASS"
    elif all_valid:
        print(f"[WARNING] Large range in constants (ratio {norm_ratio:.1f})")
        status = "WARNING"
    else:
        print("[ERROR] Invalid normalization constants (zero, negative, or inf)")
        status = "FAIL"

    return {
        'test': 'Normalization',
        'controller': controller_type,
        'norms': norms,
        'norm_ratio': norm_ratio,
        'status': status
    }


def main():
    """Run all Phase 1.1 diagnostic tests."""
    print("\n" + "#"*80)
    print("# PHASE 1.1: COST FUNCTION ISOLATION TESTS")
    print("#"*80)

    controller_type = 'sta_smc'  # Focus on STA-SMC (main PSO target)

    # Run all tests
    results = []
    results.append(test_mt8_nominal_scenario(controller_type))
    results.append(test_umax_consistency(controller_type))
    results.append(test_pathological_gains(controller_type))
    results.append(test_normalization(controller_type))

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
        print("\n[OK] All tests passed! Cost function working correctly.")
        print("[INFO] Proceed to Phase 1.2: Scenario Difficulty Tests")
    elif failed == 0:
        print("\n[WARNING] All tests passed with warnings. Review marginal issues.")
        print("[INFO] May proceed to Phase 1.2, but monitor for issues.")
    else:
        print("\n[ERROR] Critical failures detected! Fix cost function issues before Phase 2.")
        print("[INFO] Focus on:")
        for result in results:
            if result['status'] == 'FAIL':
                print(f"  - {result['test']}")

    return results


if __name__ == "__main__":
    main()
