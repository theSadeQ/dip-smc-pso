# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 14
# Runnable: False
# Hash: 9d06709e

# Lazy initialization on first stabilize entry
if not self._stabilizer_initialized:
    if hasattr(self.stabilizer, "initialize_state"):
        self._stab_state_vars = self.stabilizer.initialize_state()
    if hasattr(self.stabilizer, "initialize_history"):
        self._stab_history = self.stabilizer.initialize_history()
    self._stabilizer_initialized = True

# Delegate control to stabilizing controller
u, self._stab_state_vars, self._stab_history = self.stabilizer.compute_control(
    state,
    self._stab_state_vars,
    self._stab_history
)

# Saturate output
if np.isfinite(self.max_force):
    u = float(np.clip(u, -self.max_force, self.max_force))

return float(u), state_vars, history