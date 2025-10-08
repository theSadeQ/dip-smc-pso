# Example from: docs\controllers\mpc_technical_guide.md
# Index: 7
# Runnable: False
# Hash: 42991651

# example-metadata:
# runnable: false

def _safe_fallback(self, x₀):
    # Prefer SMC if instantiated
    if self._fallback is not None:
        try:
            u, state, history = self._fallback.compute_control(x₀, ...)
            return clip(u, -max_force, max_force)
        except:
            pass  # Degrade to PD

    # Conservative PD on angles
    θ_err = (x₀[1] - π) + (x₀[2] - π)
    θ̇_err = x₀[4] + x₀[5]
    u = -self._pd_kp * θ_err - self._pd_kd * θ̇_err
    return clip(u, -max_force, max_force)