# Example from: docs\controllers\swing_up_smc_technical_guide.md
# Index: 3
# Runnable: False
# Hash: f506054f

def _should_switch_to_stabilize(self, E_about_bottom, θ₁, θ₂):
    """
    Check if conditions met for swing → stabilize.

    Returns:
        (should_switch, high_energy, small_angles)
    """
    high_energy = (E_about_bottom >= self.switch_energy_factor * self.E_bottom)
    small_angles = (abs(θ₁) <= self.switch_angle_tol and
                   abs(θ₂) <= self.switch_angle_tol)

    should_switch = high_energy and small_angles  # ALL conditions
    return (should_switch, high_energy, small_angles)

def _should_switch_to_swing(self, E_about_bottom, θ₁, θ₂):
    """
    Check if conditions met for stabilize → swing.

    Returns:
        (should_switch, low_energy, angle_excursion)
    """
    low_energy = (E_about_bottom < self.exit_energy_factor * self.E_bottom)
    angle_excursion = (abs(θ₁) > self.reentry_angle_tol or
                      abs(θ₂) > self.reentry_angle_tol)

    should_switch = low_energy or angle_excursion  # ANY condition
    return (should_switch, low_energy, angle_excursion)