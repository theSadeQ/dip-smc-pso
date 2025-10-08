# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 22
# Runnable: True
# Hash: 609425b3

"""Example: Custom controller with PSO interface."""

import numpy as np
from src.optimization.algorithms.pso_optimizer import PSOTuner

class CustomSMC:
    """Custom SMC implementing PSO interface."""

    def __init__(self, gains: np.ndarray):
        if len(gains) != 3:
            raise ValueError("Custom SMC requires 3 gains")
        self.k1, self.k2, self.k3 = gains
        self._max_force = 100.0

    @property
    def max_force(self) -> float:
        return self._max_force

    def compute_control(self, state: np.ndarray, **kwargs) -> float:
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state

        # Custom control law
        u = -self.k1 * theta1 - self.k2 * theta2 - self.k3 * x
        return np.clip(u, -self.max_force, self.max_force)

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        # All gains must be positive
        return np.all(particles > 0, axis=1)

def optimize_custom_controller():
    """Optimize custom controller with PSO."""

    # Create factory function
    def create_custom_smc(gains: np.ndarray) -> CustomSMC:
        return CustomSMC(gains)

    # Mock configuration (normally loaded from YAML)
    class MockConfig:
        simulation = type('obj', (object,), {'duration': 10.0, 'dt': 0.001})
        cost_function = type('obj', (object,), {
            'weights': type('obj', (object,), {
                'state_error': 1.0, 'control_effort': 0.01,
                'control_rate': 0.001, 'stability': 10.0
            })()
        })()

    # Initialize PSO tuner
    pso_tuner = PSOTuner(
        controller_factory=create_custom_smc,
        config=MockConfig(),
        seed=42
    )

    # Optimize
    bounds = (np.array([0.1, 0.1, 0.1]), np.array([10.0, 10.0, 10.0]))
    results = pso_tuner.optimize(bounds=bounds, n_particles=20, n_iterations=50)

    return results