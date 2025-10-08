# Example from: docs\testing\reports\2025-09-30\pso_fitness_investigation.md
# Index: 5
# Runnable: True
# Hash: 906796c8

#==========================================================================================\\\
#========================= scripts/debug_pso_fitness.py =================================\\\
#==========================================================================================\\\

"""PSO Fitness Function Diagnostic Tool"""

import numpy as np
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

def diagnose_normalization():
    """Diagnose normalization effects"""
    config = load_config("config.yaml")

    # Create PSOTuner (triggers baseline normalization)
    def dummy_factory(gains):
        from src.controllers.smc.classic_smc import ClassicalSMC
        return ClassicalSMC(gains=gains, max_force=100.0)

    tuner = PSOTuner(dummy_factory, config)

    # Print normalization constants
    print("=" * 90)
    print("PSO NORMALIZATION DIAGNOSTIC")
    print("=" * 90)
    print(f"\nNormalization Constants:")
    print(f"  norm_ise:    {tuner.norm_ise:.6e}")
    print(f"  norm_u:      {tuner.norm_u:.6e}")
    print(f"  norm_du:     {tuner.norm_du:.6e}")
    print(f"  norm_sigma:  {tuner.norm_sigma:.6e}")

    print(f"\nCost Weights:")
    print(f"  state_error:     {tuner.weights.state_error}")
    print(f"  control_effort:  {tuner.weights.control_effort}")
    print(f"  control_rate:    {tuner.weights.control_rate}")
    print(f"  stability:       {tuner.weights.stability}")

    print(f"\nInstability Penalty: {tuner.instability_penalty:.6e}")
    print(f"Combine Weights: mean={tuner.combine_weights[0]}, max={tuner.combine_weights[1]}")

    # Simulate example cost computation
    print(f"\n{'=' * 90}")
    print("EXAMPLE COST COMPUTATION")
    print("=" * 90)

    # Example raw costs
    ise_raw = 1.0      # Good tracking
    u_sq_raw = 50.0    # Moderate control effort
    du_sq_raw = 100.0  # Moderate slew rate
    sigma_sq_raw = 0.5 # Good sliding surface convergence

    # Normalize
    ise_n = ise_raw / tuner.norm_ise if tuner.norm_ise > 1e-12 else ise_raw
    u_n = u_sq_raw / tuner.norm_u if tuner.norm_u > 1e-12 else u_sq_raw
    du_n = du_sq_raw / tuner.norm_du if tuner.norm_du > 1e-12 else du_sq_raw
    sigma_n = sigma_sq_raw / tuner.norm_sigma if tuner.norm_sigma > 1e-12 else sigma_sq_raw

    print(f"\nRaw Costs:")
    print(f"  ISE:     {ise_raw:.4f}  →  Normalized: {ise_n:.6e}")
    print(f"  U²:      {u_sq_raw:.4f}  →  Normalized: {u_n:.6e}")
    print(f"  (ΔU)²:   {du_sq_raw:.4f}  →  Normalized: {du_n:.6e}")
    print(f"  σ²:      {sigma_sq_raw:.4f}  →  Normalized: {sigma_n:.6e}")

    # Compute weighted cost
    J_components = {
        'state_error': tuner.weights.state_error * ise_n,
        'control_effort': tuner.weights.control_effort * u_n,
        'control_rate': tuner.weights.control_rate * du_n,
        'stability': tuner.weights.stability * sigma_n
    }

    J_total = sum(J_components.values())

    print(f"\nWeighted Cost Components:")
    for name, value in J_components.items():
        pct = (value / J_total * 100) if J_total > 0 else 0
        print(f"  {name:20s}: {value:.6e}  ({pct:.1f}%)")

    print(f"\nTotal Cost: {J_total:.6e}")

    print(f"\n{'=' * 90}")
    print("ASSESSMENT")
    print("=" * 90)

    # Assess normalization health
    if tuner.norm_ise > 100.0:
        print("⚠️  WARNING: norm_ise is very large - may cause excessive normalization")
    if tuner.weights.state_error > 10.0:
        print("⚠️  WARNING: state_error weight is very high - may dominate cost")
    if J_total < 1e-3:
        print("🔴 CRITICAL: Total cost is near zero - PSO cannot distinguish particles")
    else:
        print("✅ Cost function sensitivity appears reasonable")

if __name__ == "__main__":
    diagnose_normalization()