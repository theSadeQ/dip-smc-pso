# Example from: docs\mathematical_foundations\sliding_surface_analysis.md
# Index: 1
# Runnable: False
# Hash: 4b412593

def _validate_gains(self) -> None:
    """Validate gain vector according to SMC theory."""
    if len(self.gains) != 6:
        raise ValueError("Classical SMC requires exactly 6 gains: [k1, k2, lam1, lam2, K, kd]")

    k1, k2, lam1, lam2, K, kd = self.gains

    # Surface gains must be positive for Hurwitz stability
    if any(g <= 0 for g in [k1, k2, lam1, lam2]):
        raise ValueError("Surface gains [k1, k2, λ1, λ2] must be positive for stability")

    # Switching gain must be positive for reaching condition
    if K <= 0:
        raise ValueError("Switching gain K must be positive")

    # Derivative gain must be non-negative
    if kd < 0:
        raise ValueError("Derivative gain kd must be non-negative")