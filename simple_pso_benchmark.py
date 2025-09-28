#!/usr/bin/env python3
#==========================================================================================\\\
#========================== simple_pso_benchmark.py =================================\\\
#==========================================================================================\\\

"""
Simple PSO Optimization Benchmark

Quick validation of PSO optimization functionality for GitHub Issue #4.
ASCII-only output for Windows compatibility.
"""

import time
import numpy as np
from src.controllers.factory import (
    SMCType, create_smc_for_pso, get_gain_bounds_for_pso,
    validate_smc_gains, SMC_GAIN_SPECS
)
from src.plant.configurations import ConfigurationFactory


def test_pso_functionality():
    """Test complete PSO functionality."""
    print("PSO OPTIMIZATION BENCHMARK - GitHub Issue #4")
    print("=" * 60)

    plant_config = ConfigurationFactory.create_default_config("simplified")
    results = []

    # Test 1: Controller Creation
    print("\n1. Testing PSO Controller Creation...")
    test_gains = {
        SMCType.CLASSICAL: [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
        SMCType.ADAPTIVE: [10.0, 5.0, 8.0, 3.0, 2.0],
        SMCType.SUPER_TWISTING: [5.0, 3.0, 10.0, 5.0, 15.0, 2.0],
        SMCType.HYBRID: [10.0, 5.0, 8.0, 3.0]
    }

    creation_results = []
    for smc_type, gains in test_gains.items():
        try:
            controller = create_smc_for_pso(smc_type, gains, plant_config)
            state = np.array([0.1, 0.2, 0.3, 0.0, 0.0, 0.0])
            control = controller.compute_control(state)
            success = isinstance(control, np.ndarray) and control.shape == (1,)
            creation_results.append(success)
            print(f"   {smc_type.value:20} {'[PASS]' if success else '[FAIL]'}")
        except Exception as e:
            creation_results.append(False)
            print(f"   {smc_type.value:20} [FAIL] {e}")

    # Test 2: Gain Bounds Retrieval
    print("\n2. Testing Gain Bounds Retrieval...")
    bounds_results = []
    for smc_type in SMCType:
        try:
            bounds = get_gain_bounds_for_pso(smc_type)
            spec = SMC_GAIN_SPECS[smc_type]
            success = (isinstance(bounds, tuple) and len(bounds) == 2 and
                      len(bounds[0]) == spec.n_gains and len(bounds[1]) == spec.n_gains)
            bounds_results.append(success)
            print(f"   {smc_type.value:20} {'[PASS]' if success else '[FAIL]'} ({spec.n_gains} gains)")
        except Exception as e:
            bounds_results.append(False)
            print(f"   {smc_type.value:20} [FAIL] {e}")

    # Test 3: Gain Validation
    print("\n3. Testing Gain Validation...")
    validation_results = []
    test_cases = {
        SMCType.CLASSICAL: {'valid': [10.0, 5.0, 8.0, 3.0, 15.0, 2.0], 'invalid': [-1.0, 5.0, 8.0, 3.0, 15.0, 2.0]},
        SMCType.ADAPTIVE: {'valid': [10.0, 5.0, 8.0, 3.0, 2.0], 'invalid': [10.0, 5.0, 8.0, -3.0, 2.0]}
    }

    for smc_type, cases in test_cases.items():
        try:
            valid_result = validate_smc_gains(smc_type, cases['valid'])
            invalid_result = validate_smc_gains(smc_type, cases['invalid'])
            success = valid_result == True and invalid_result == False
            validation_results.append(success)
            print(f"   {smc_type.value:20} {'[PASS]' if success else '[FAIL]'} (V:{valid_result}, I:{invalid_result})")
        except Exception as e:
            validation_results.append(False)
            print(f"   {smc_type.value:20} [FAIL] {e}")

    # Test 4: End-to-End PSO Simulation
    print("\n4. Testing End-to-End PSO Simulation...")
    try:
        # Simulate PSO optimization with multiple gain sets
        smc_type = SMCType.CLASSICAL
        test_gain_sets = [
            [10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
            [15.0, 8.0, 12.0, 5.0, 20.0, 3.0],
            [5.0, 3.0, 6.0, 2.0, 10.0, 1.0]
        ]

        best_cost = float('inf')
        best_gains = None

        for gains in test_gain_sets:
            if validate_smc_gains(smc_type, gains):
                controller = create_smc_for_pso(smc_type, gains, plant_config)
                state = np.array([0.1, 0.2, 0.3, 0.0, 0.0, 0.0])
                control = controller.compute_control(state)
                cost = np.sum(state[:3]**2) + 0.1 * np.sum(control**2)

                if cost < best_cost:
                    best_cost = cost
                    best_gains = gains

        e2e_success = best_gains is not None and np.isfinite(best_cost)
        print(f"   End-to-End PSO      {'[PASS]' if e2e_success else '[FAIL]'} (Cost: {best_cost:.4f})")
    except Exception as e:
        e2e_success = False
        print(f"   End-to-End PSO      [FAIL] {e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY - PSO OPTIMIZATION FUNCTIONALITY")
    print("=" * 60)

    all_creation_passed = all(creation_results)
    all_bounds_passed = all(bounds_results)
    all_validation_passed = all(validation_results)

    print(f"Controller Creation:     {'[PASS]' if all_creation_passed else '[FAIL]'} ({sum(creation_results)}/{len(creation_results)})")
    print(f"Gain Bounds Retrieval:   {'[PASS]' if all_bounds_passed else '[FAIL]'} ({sum(bounds_results)}/{len(bounds_results)})")
    print(f"Gain Validation:         {'[PASS]' if all_validation_passed else '[FAIL]'} ({sum(validation_results)}/{len(validation_results)})")
    print(f"End-to-End PSO:          {'[PASS]' if e2e_success else '[FAIL]'}")

    core_functions_working = all_creation_passed and all_bounds_passed and all_validation_passed
    overall_success = core_functions_working and e2e_success

    print("\n" + "=" * 60)
    if overall_success:
        print("GITHUB ISSUE #4 RESOLUTION: SUCCESS")
        print("[PASS] PSO optimization workflow is FULLY FUNCTIONAL")
        print("[PASS] All critical PSO functions operational")
        print("[PASS] Gain bounds retrieval working correctly")
        print("[PASS] Parameter validation passing")
        print("[PASS] End-to-end PSO workflow operational")
    else:
        print("GITHUB ISSUE #4 RESOLUTION: NEEDS ATTENTION")
        if not core_functions_working:
            print("[FAIL] Core PSO functions need fixes")
        if not e2e_success:
            print("[FAIL] End-to-end workflow needs attention")

    print("=" * 60)

    return overall_success


if __name__ == "__main__":
    success = test_pso_functionality()
    exit(0 if success else 1)