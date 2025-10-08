# Example from: docs\technical\mathematical_foundations.md
# Index: 2
# Runnable: False
# Hash: 2b3f91b0

def validate_super_twisting_gains(gains):
    """Validate Super-Twisting SMC gains for finite-time stability."""

    K1, K2, c1, lam1, c2, lam2 = gains

    # Finite-time stability condition
    assert K1 > K2 > 0, "Must have K1 > K2 > 0 for finite-time stability"

    # Sufficient condition for robust finite-time stability
    # Assumes worst-case Lipschitz constant α = 1.0
    assert K1**2 > 2.0, "K1² > 2α required for robust finite-time convergence"

    # Surface design validation (same as classical)
    assert c1 > 0 and c2 > 0, "Surface position gains must be positive"
    assert lam1 > 0 and lam2 > 0, "Surface velocity gains must be positive"