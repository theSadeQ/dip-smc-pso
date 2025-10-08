# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 15
# Runnable: False
# Hash: dc2e29b2

# Validate hysteresis band
if self.exit_energy_factor >= self.switch_energy_factor:
    raise ValueError(
        "exit_energy_factor must be < switch_energy_factor to create deadband"
    )

# Validate angle tolerance ordering
if self.reentry_angle_tol < self.switch_angle_tol:
    raise ValueError(
        "reentry_angle_tolerance should be >= switch_angle_tolerance"
    )