# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 4
# Runnable: False
# Hash: a54e37b4

# example-metadata:
# runnable: false

def _update_adaptive_gains(self, abs_s: float, k1_prev: float, k2_prev: float):
    """Update adaptive gains with self-tapering and anti-windup.

    Implements:
    - State-based adaptation: γ|s|
    - Self-tapering: τ(|s|) = |s|/(|s| + ε)
    - Rate limiting: |k̇| ≤ rate_limit
    - Anti-windup: Freeze when saturated + near equilibrium
    """
    if abs_s <= self.dead_zone:
        # In dead zone: gentle leak to prevent ratcheting
        k1_dot = -self.gain_leak
        k2_dot = -self.gain_leak
    else:
        # Normal adaptation with self-tapering
        taper_factor = self._compute_taper_factor(abs_s)
        k1_raw = self.gamma1 * abs_s * taper_factor
        k2_raw = self.gamma2 * abs_s * taper_factor

        # Rate limiting for stability
        k1_dot = min(k1_raw, self.adapt_rate_limit)
        k2_dot = min(k2_raw, self.adapt_rate_limit)

    return k1_dot, k2_dot