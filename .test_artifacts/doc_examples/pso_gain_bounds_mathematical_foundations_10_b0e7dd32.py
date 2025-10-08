# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 10
# Runnable: True
# Hash: b0e7dd32

STA_SMC_BOUNDS_ISSUE2 = {
    'K1': (1.0, 100.0),      # First-order STA gain
    'K2': (1.0, 100.0),      # Second-order STA gain (K1 > K2)
    'k1': (1.0, 20.0),       # Surface gain
    'k2': (1.0, 20.0),       # Surface gain
    'lambda1': (0.1, 10.0),  # Surface coefficient (Issue #2 optimized)
    'lambda2': (0.1, 10.0)   # Surface coefficient (Issue #2 optimized)
}