#!/usr/bin/env python
"""
Quick test to verify parallel speedup BEFORE running full PSO.
Tests both sequential and parallel evaluation to measure actual speedup.

Usage:
    python test_parallel_speedup.py

Expected output:
    Sequential: 30-40 seconds for 25 particles
    Parallel: 3-8 seconds for 25 particles
    Speedup: 5-12x

If speedup < 2x, parallel mode may not help on your system.
"""

import sys
import time
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from scripts.phase2_bulletproof_pso_v2 import (
    create_robust_cost_evaluator_wrapper,
    evaluate_particles_parallel
)


def main():
    print("="*80)
    print("PARALLEL PSO SPEEDUP TEST - 5 MINUTE VERIFICATION")
    print("="*80)
    print()

    # Load config
    config = load_config("config.yaml")

    # Create cost function (STA-SMC as example)
    print("[1/4] Creating cost evaluator (5 scenarios)...")
    cost_fn = create_robust_cost_evaluator_wrapper('sta_smc', config)
    print("[OK] Cost evaluator ready")
    print()

    # Generate 25 random particle positions (6 gains for STA-SMC)
    print("[2/4] Generating 25 random test particles...")
    n_particles = 25
    n_gains = 6
    bounds_min = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    bounds_max = np.array([15.0, 15.0, 15.0, 15.0, 15.0, 15.0])

    rng = np.random.default_rng(42)
    test_particles = rng.uniform(bounds_min, bounds_max, size=(n_particles, n_gains))
    print(f"[OK] Generated {n_particles} particles")
    print()

    # Test 1: Sequential evaluation
    print(f"[3/4] Testing SEQUENTIAL evaluation ({n_particles} particles)...")
    print("       This will take 30-60 seconds...")
    start_seq = time.time()

    costs_seq = []
    for i in range(n_particles):
        cost = cost_fn(test_particles[i])
        costs_seq.append(cost)
        if (i+1) % 5 == 0:
            print(f"       Progress: {i+1}/{n_particles} particles ({(i+1)/n_particles*100:.0f}%)")

    time_seq = time.time() - start_seq
    print(f"[OK] Sequential time: {time_seq:.2f} seconds")
    print()

    # Test 2: Parallel evaluation
    n_workers = max(1, cpu_count() - 1)
    print(f"[4/4] Testing PARALLEL evaluation ({n_particles} particles, {n_workers} workers)...")
    print("       This should be much faster...")
    start_par = time.time()

    costs_par = evaluate_particles_parallel(test_particles, cost_fn, n_workers)

    time_par = time.time() - start_par
    print(f"[OK] Parallel time: {time_par:.2f} seconds")
    print()

    # Results
    speedup = time_seq / time_par
    print("="*80)
    print("RESULTS")
    print("="*80)
    print(f"Sequential time:  {time_seq:.2f} sec")
    print(f"Parallel time:    {time_par:.2f} sec")
    print(f"Speedup:          {speedup:.2f}x")
    print(f"Workers:          {n_workers}")
    print()

    # Verify costs match (should be identical)
    cost_diff = np.abs(np.array(costs_seq) - costs_par).max()
    print(f"Cost verification: max difference = {cost_diff:.6f} (should be ~0)")
    print()

    # Interpretation
    print("="*80)
    print("INTERPRETATION")
    print("="*80)

    if speedup >= 5:
        print("[EXCELLENT] 5x+ speedup! Parallel mode will MASSIVELY speed up PSO.")
        print(f"Expected PSO time: 15 hours / {speedup:.1f} = {15/speedup:.1f} hours")
    elif speedup >= 3:
        print("[GOOD] 3-5x speedup. Parallel mode will significantly speed up PSO.")
        print(f"Expected PSO time: 15 hours / {speedup:.1f} = {15/speedup:.1f} hours")
    elif speedup >= 2:
        print("[OK] 2-3x speedup. Parallel mode helps but not dramatically.")
        print(f"Expected PSO time: 15 hours / {speedup:.1f} = {15/speedup:.1f} hours")
    else:
        print("[WARNING] <2x speedup. Parallel overhead may be limiting gains.")
        print("Possible issues:")
        print("  - Few CPU cores (check: cpu_count())")
        print("  - High multiprocessing overhead")
        print("  - Consider --no-parallel and reduce iterations/particles instead")

    print()
    print("="*80)
    print(f"Test complete! Speedup: {speedup:.2f}x on your system")
    print("="*80)


if __name__ == '__main__':
    main()
