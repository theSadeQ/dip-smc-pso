# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 21
# Runnable: True
# Hash: f5365fe9

if any(g <= 0 for g in [k1, k2, lam1, lam2]):
    raise ValueError("Surface gains must be positive for stability")