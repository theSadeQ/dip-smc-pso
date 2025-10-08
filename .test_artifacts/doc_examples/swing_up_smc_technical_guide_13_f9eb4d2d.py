# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 13
# Runnable: True
# Hash: f9eb4d2d

if self._mode == SWING_MODE:
    # Energy pumping control law
    u = self.k_swing * np.cos(θ₁) * θ̇₁

    # Saturate to actuator limits
    if np.isfinite(self.max_force):
        u = float(np.clip(u, -self.max_force, self.max_force))

    return float(u), state_vars, history