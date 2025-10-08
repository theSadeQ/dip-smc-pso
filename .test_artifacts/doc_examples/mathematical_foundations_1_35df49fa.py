# Example from: docs\technical\mathematical_foundations.md
# Index: 1
# Runnable: False
# Hash: 35df49fa

# example-metadata:
# runnable: false

def validate_classical_smc_gains(gains):
    """Validate Classical SMC gains against mathematical requirements."""

    c1, c2, lam1, lam2, K, kd = gains

    # Hurwitz stability conditions
    assert c1 > 0, "Surface gain c1 must be positive for Hurwitz stability"
    assert c2 > 0, "Surface gain c2 must be positive for Hurwitz stability"
    assert lam1 > 0, "Velocity gain λ1 must be positive for Hurwitz stability"
    assert lam2 > 0, "Velocity gain λ2 must be positive for Hurwitz stability"

    # Switching gain positivity
    assert K > 0, "Switching gain K must be positive for reaching condition"

    # Derivative gain non-negativity
    assert kd >= 0, "Derivative gain kd must be non-negative"

    # Numerical stability bounds
    assert all(1e-12 <= g <= 1e5 for g in gains[:5]), "Gains must be in numerically stable range"