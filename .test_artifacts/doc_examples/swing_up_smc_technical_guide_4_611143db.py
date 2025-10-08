# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 4
# Runnable: False
# Hash: 611143db

def _update_mode(self, E_about_bottom, θ₁, θ₂, t, history):
    """Evaluate and execute mode transitions."""
    if self._mode == SWING_MODE:
        should, high_energy, small_angles = self._should_switch_to_stabilize(...)
        if should:
            self._mode = STABILIZE_MODE
            self._switch_time = t  # Record handoff time
            logger.info("swing → stabilize at t=%.3fs", t)

    elif self._mode == STABILIZE_MODE:
        should, low_energy, angle_excursion = self._should_switch_to_swing(...)
        if should:
            self._mode = SWING_MODE
            logger.info("stabilize → swing at t=%.3fs", t)