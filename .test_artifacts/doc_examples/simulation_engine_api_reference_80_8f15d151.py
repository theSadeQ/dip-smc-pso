# Example from: docs\api\simulation_engine_api_reference.md
# Index: 80
# Runnable: True
# Hash: 8f15d151

def _guard_energy(state: np.ndarray, config: Any) -> None:
    """Check total energy within bounds."""
    E_kinetic = 0.5 * m * (x_dot**2 + theta1_dot**2 + theta2_dot**2)
    E_potential = m * g * (L1 * cos(theta1) + L2 * cos(theta2))
    E_total = E_kinetic + E_potential

    if E_total > config.safety.max_energy:
        raise SafetyViolationError(f"Energy {E_total:.2f}J exceeds {config.safety.max_energy}J")