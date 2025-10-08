# Example from: docs\api\factory_methods_reference.md
# Index: 47
# Runnable: True
# Hash: c711ca81

#!/usr/bin/env python3
"""PSO integration examples."""

from src.controllers.factory import (
    create_pso_controller_factory,
    get_gain_bounds_for_pso,
    validate_smc_gains,
    SMCType
)
import numpy as np

def pso_integration_example():
    """Demonstrate PSO integration patterns."""

    # Get optimization bounds
    bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
    lower_bounds, upper_bounds = bounds
    print(f"Optimization bounds: {lower_bounds} to {upper_bounds}")

    # Create PSO-optimized factory
    factory = create_pso_controller_factory(SMCType.CLASSICAL)
    print(f"Factory requires {factory.n_gains} gains")

    # Define fitness function
    def fitness_function(gains: np.ndarray) -> float:
        """PSO fitness function with validation."""

        # Pre-validate gains
        if not validate_smc_gains(SMCType.CLASSICAL, gains):
            return float('inf')

        try:
            # Create controller
            controller = factory(gains)

            # Simplified performance evaluation
            test_state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
            control_output = controller.compute_control(test_state)

            # Simple fitness (control effort)
            return abs(control_output.u) if hasattr(control_output, 'u') else abs(control_output)

        except Exception:
            return float('inf')

    # Test fitness function
    test_gains = np.array([20.0, 15.0, 12.0, 8.0, 35.0, 5.0])
    fitness = fitness_function(test_gains)
    print(f"Test fitness: {fitness}")

    # Simulate PSO particle validation
    particles = np.random.uniform(
        low=lower_bounds,
        high=upper_bounds,
        size=(10, len(lower_bounds))
    )

    valid_particles = []
    for particle in particles:
        if validate_smc_gains(SMCType.CLASSICAL, particle):
            valid_particles.append(particle)

    print(f"Valid particles: {len(valid_particles)}/{len(particles)}")

if __name__ == "__main__":
    pso_integration_example()