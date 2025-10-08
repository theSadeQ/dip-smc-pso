# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 5
# Runnable: False
# Hash: c205fead

# example-metadata:
# runnable: false

def compute_control(self, state, state_vars, history):
    """
    Compute control based on current mode.

    Args:
        state: [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
        state_vars: Controller state (unused for swing-up)
        history: Dict with mode tracking

    Returns:
        (u, state_vars, history)
    """
    θ₁, θ₂, θ̇₁ = state[1], state[2], state[4]

    # Compute current energy
    E_current = self.dynamics.total_energy(state)
    E_about_bottom = self.E_bottom - E_current

    # Track normalized energy for telemetry
    history["E_ratio"] = E_about_bottom / self.E_bottom

    # Update time
    t = history.get("t", 0.0) + self.dt
    history["t"] = t

    # Evaluate mode transitions
    self._update_mode(E_about_bottom, θ₁, θ₂, t, history)

    # --- Swing Mode ---
    if self._mode == SWING_MODE:
        u = self.k_swing * np.cos(θ₁) * θ̇₁
        u = np.clip(u, -self.max_force, self.max_force)
        return (u, state_vars, history)

    # --- Stabilize Mode ---
    # Initialize stabilizer state on first entry
    if not self._stabilizer_initialized:
        if hasattr(self.stabilizer, "initialize_state"):
            self._stab_state_vars = self.stabilizer.initialize_state()
        if hasattr(self.stabilizer, "initialize_history"):
            self._stab_history = self.stabilizer.initialize_history()
        self._stabilizer_initialized = True

    # Delegate to stabilizing controller
    u, self._stab_state_vars, self._stab_history = self.stabilizer.compute_control(
        state, self._stab_state_vars, self._stab_history
    )
    u = np.clip(u, -self.max_force, self.max_force)
    return (u, state_vars, history)