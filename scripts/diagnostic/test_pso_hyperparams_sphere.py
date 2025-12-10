#======================================================================================\
#================= scripts/diagnostic/test_pso_hyperparams_sphere.py ===============\
#======================================================================================\
"""
Phase 1.4: PSO Hyperparameters Sphere Test

Tests PSO algorithm on simple 6D sphere function to validate hyperparameters:
1. Convergence test: f(x) = sum(x^2), should reach <0.01 in 50 iterations
2. Narrow vs wide bounds: narrow should converge 2x faster
3. Swarm size adequacy: 25 vs 40 particles (<10% difference)

Usage:
    python scripts/diagnostic/test_pso_hyperparams_sphere.py

Expected Results:
    [OK] Sphere converges to <0.01 in 50 iters
    [OK] Narrow bounds >=50% faster
    [OK] 25 particles adequate

Author: Claude Code
Date: December 2025
"""

import numpy as np
import sys
from pathlib import Path
from typing import Dict, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def sphere_function(x: np.ndarray) -> float:
    """6D sphere function: f(x) = sum(x^2), optimum at [0,0,0,0,0,0]."""
    return float(np.sum(x**2))


def pso_optimize(
    cost_fn,
    bounds: Tuple[np.ndarray, np.ndarray],
    n_particles: int = 25,
    max_iters: int = 50,
    w_start: float = 0.9,
    w_end: float = 0.4,
    c1: float = 1.5,
    c2: float = 2.0,
    seed: int = 42
) -> Dict:
    """Simple PSO implementation matching phase2_bulletproof_pso_v2.py settings."""
    rng = np.random.default_rng(seed)
    min_bounds, max_bounds = bounds
    n_dims = len(min_bounds)

    # Initialize swarm
    particles = min_bounds + rng.random((n_particles, n_dims)) * (max_bounds - min_bounds)
    velocities = np.zeros((n_particles, n_dims))

    # Evaluate initial swarm
    costs = np.array([cost_fn(p) for p in particles])
    personal_best_positions = particles.copy()
    personal_best_costs = costs.copy()

    # Global best
    global_best_idx = np.argmin(costs)
    global_best_position = particles[global_best_idx].copy()
    global_best_cost = costs[global_best_idx]

    # Track convergence
    history = [global_best_cost]

    # Velocity clamping
    vel_min = 0.1 * (max_bounds - min_bounds)
    vel_max = 0.5 * (max_bounds - min_bounds)

    for iteration in range(max_iters):
        # Adaptive inertia weight (linear decay)
        w = w_start - (w_start - w_end) * (iteration / max_iters)

        for i in range(n_particles):
            # Update velocity
            r1, r2 = rng.random(n_dims), rng.random(n_dims)
            cognitive = c1 * r1 * (personal_best_positions[i] - particles[i])
            social = c2 * r2 * (global_best_position - particles[i])
            velocities[i] = w * velocities[i] + cognitive + social

            # Clamp velocity
            velocities[i] = np.clip(velocities[i], -vel_max, vel_max)

            # Update position
            particles[i] = particles[i] + velocities[i]
            particles[i] = np.clip(particles[i], min_bounds, max_bounds)

            # Evaluate
            cost = cost_fn(particles[i])
            costs[i] = cost

            # Update personal best
            if cost < personal_best_costs[i]:
                personal_best_costs[i] = cost
                personal_best_positions[i] = particles[i].copy()

                # Update global best
                if cost < global_best_cost:
                    global_best_cost = cost
                    global_best_position = particles[i].copy()

        history.append(global_best_cost)

    return {
        'best_position': global_best_position,
        'best_cost': global_best_cost,
        'history': history,
        'iterations': max_iters
    }


def test_sphere_convergence() -> Dict:
    """Test 1: Convergence on 6D sphere function.

    Expected: Converge to <0.01 in 50 iterations
    If >0.1: PSO hyperparams inadequate
    """
    print("\n" + "="*80)
    print("TEST 1: Sphere Function Convergence")
    print("="*80)

    print("\nOptimizing 6D sphere: f(x) = sum(x^2)")
    print("Optimum: [0,0,0,0,0,0], f* = 0.0")
    print("Bounds: [-10, 10] per dimension")
    print("PSO settings: w=[0.9->0.4], c1=1.5, c2=2.0, n=25, iters=50")

    # Run PSO
    bounds = (np.array([-10.0] * 6), np.array([10.0] * 6))
    result = pso_optimize(
        sphere_function,
        bounds,
        n_particles=25,
        max_iters=50,
        w_start=0.9,
        w_end=0.4,
        c1=1.5,
        c2=2.0,
        seed=42
    )

    print(f"\n[INFO] Results:")
    print(f"  Best cost: {result['best_cost']:.6f}")
    print(f"  Best position: {result['best_position']}")
    print(f"  Initial cost: {result['history'][0]:.6f}")
    print(f"  Final cost: {result['history'][-1]:.6f}")

    # Check convergence milestones
    iter_10 = result['history'][10]
    iter_25 = result['history'][25]
    iter_50 = result['history'][50]

    print(f"\n[INFO] Convergence milestones:")
    print(f"  Iteration 10: {iter_10:.6f}")
    print(f"  Iteration 25: {iter_25:.6f}")
    print(f"  Iteration 50: {iter_50:.6f}")

    # Validate
    if iter_50 < 0.01:
        print("\n[OK] PSO converges to <0.01 in 50 iters")
        status = "PASS"
    elif iter_50 < 0.1:
        print(f"\n[WARNING] Slow convergence (final: {iter_50:.6f})")
        status = "WARNING"
    else:
        print(f"\n[ERROR] PSO failed to converge! Final: {iter_50:.6f}")
        status = "FAIL"

    return {
        'test': 'Sphere Convergence',
        'final_cost': iter_50,
        'iterations': 50,
        'status': status
    }


def test_narrow_vs_wide_bounds() -> Dict:
    """Test 2: Narrow vs wide bounds comparison.

    Expected: Narrow bounds converge >=50% faster
    If <30%: bounds don't matter much (unexpected)
    """
    print("\n" + "="*80)
    print("TEST 2: Narrow vs Wide Bounds")
    print("="*80)

    print("\nComparing convergence speed:")
    print("  Narrow: [-5, 5] per dimension")
    print("  Wide: [-15, 15] per dimension")

    # Narrow bounds
    bounds_narrow = (np.array([-5.0] * 6), np.array([5.0] * 6))
    result_narrow = pso_optimize(
        sphere_function,
        bounds_narrow,
        n_particles=25,
        max_iters=50,
        seed=42
    )

    # Wide bounds
    bounds_wide = (np.array([-15.0] * 6), np.array([15.0] * 6))
    result_wide = pso_optimize(
        sphere_function,
        bounds_wide,
        n_particles=25,
        max_iters=50,
        seed=42
    )

    # Find iteration where each reaches 0.1
    iter_narrow = next((i for i, c in enumerate(result_narrow['history']) if c < 0.1), 50)
    iter_wide = next((i for i, c in enumerate(result_wide['history']) if c < 0.1), 50)

    speedup = (iter_wide - iter_narrow) / iter_narrow * 100 if iter_narrow > 0 else 0

    print(f"\n[INFO] Results:")
    print(f"  Narrow final: {result_narrow['best_cost']:.6f}")
    print(f"  Wide final: {result_wide['best_cost']:.6f}")
    print(f"  Narrow iterations to 0.1: {iter_narrow}")
    print(f"  Wide iterations to 0.1: {iter_wide}")
    print(f"  Speedup: {speedup:.1f}%")

    # Validate
    if speedup >= 50.0:
        print(f"\n[OK] Narrow bounds {speedup:.1f}% faster (>=50%)")
        status = "PASS"
    elif speedup >= 30.0:
        print(f"\n[WARNING] Moderate speedup ({speedup:.1f}%)")
        status = "WARNING"
    else:
        print(f"\n[ERROR] Narrow bounds not beneficial ({speedup:.1f}% < 30%)")
        status = "FAIL"

    return {
        'test': 'Narrow vs Wide Bounds',
        'speedup_percent': speedup,
        'narrow_iters': iter_narrow,
        'wide_iters': iter_wide,
        'status': status
    }


def test_swarm_size_adequacy() -> Dict:
    """Test 3: Swarm size adequacy.

    Expected: 25 particles adequate (40 gives <10% improvement)
    If 40 is >20% better: need larger swarm
    """
    print("\n" + "="*80)
    print("TEST 3: Swarm Size Adequacy")
    print("="*80)

    print("\nComparing swarm sizes:")
    print("  Small: 25 particles")
    print("  Large: 40 particles")

    # 25 particles
    bounds = (np.array([-10.0] * 6), np.array([10.0] * 6))
    result_25 = pso_optimize(
        sphere_function,
        bounds,
        n_particles=25,
        max_iters=50,
        seed=42
    )

    # 40 particles
    result_40 = pso_optimize(
        sphere_function,
        bounds,
        n_particles=40,
        max_iters=50,
        seed=42
    )

    improvement = (result_25['best_cost'] - result_40['best_cost']) / result_25['best_cost'] * 100
    improvement = max(0, improvement)  # Negative means 40 is worse

    print(f"\n[INFO] Results:")
    print(f"  25 particles: {result_25['best_cost']:.6f}")
    print(f"  40 particles: {result_40['best_cost']:.6f}")
    print(f"  Improvement with 40: {improvement:.1f}%")

    # Validate
    if improvement < 10.0:
        print(f"\n[OK] 25 particles adequate (40 only {improvement:.1f}% better)")
        status = "PASS"
    elif improvement < 20.0:
        print(f"\n[WARNING] 40 particles moderately better ({improvement:.1f}%)")
        status = "WARNING"
    else:
        print(f"\n[ERROR] Need larger swarm! 40 is {improvement:.1f}% better")
        status = "FAIL"

    return {
        'test': 'Swarm Size Adequacy',
        'improvement_percent': improvement,
        'cost_25': result_25['best_cost'],
        'cost_40': result_40['best_cost'],
        'status': status
    }


def main():
    """Run all Phase 1.4 diagnostic tests."""
    print("\n" + "#"*80)
    print("# PHASE 1.4: PSO HYPERPARAMETERS SPHERE TEST")
    print("#"*80)

    # Run all tests
    results = []
    results.append(test_sphere_convergence())
    results.append(test_narrow_vs_wide_bounds())
    results.append(test_swarm_size_adequacy())

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
        print("\n[OK] All tests passed! PSO hyperparameters validated.")
        print("[INFO] Phase 2 PSO settings (w=[0.9->0.4], c1=1.5, c2=2.0) confirmed.")
    elif failed == 0:
        print("\n[WARNING] Tests passed with warnings. Hyperparameters acceptable.")
    else:
        print("\n[ERROR] Critical failures! PSO hyperparameters may need adjustment.")
        print("[INFO] Consider:")
        print("  - Standard PSO: w=0.9 fixed, c1=c2=2.0")
        print("  - Larger swarm: 40 particles")
        print("  - More iterations: 100-200")

    return results


if __name__ == "__main__":
    main()
