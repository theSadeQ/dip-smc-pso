# Example from: docs\guides\workflows\pso-sta-smc.md
# Index: 2
# Runnable: False
# Hash: 0c2b238e

optimized_gains = [
    23.67,  # K1: 2.96× increase → stronger convergence
    13.29,  # K2: 3.32× increase → better robustness
    8.87,   # k1: 0.74× (decreased) → less aggressive surface
    3.55,   # k2: 0.59× (decreased) → smoother dynamics
    6.52,   # λ1: 1.34× increase → moderate damping
    2.93    # λ2: 0.85× (decreased) → refined tuning
]

# Saved to: optimized_gains_sta_smc_phase53.json
# Best Cost: 0.000000