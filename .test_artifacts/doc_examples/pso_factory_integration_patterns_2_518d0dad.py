# Example from: docs\pso_factory_integration_patterns.md
# Index: 2
# Runnable: True
# Hash: 518d0dad

from src.controllers.factory import create_pso_controller_factory, SMCType

def optimized_pso_workflow():
    """High-performance PSO workflow using factory function pattern."""

    # Create factory function once (expensive operation)
    controller_factory = create_pso_controller_factory(
        SMCType.CLASSICAL,
        plant_config=config.physics,
        max_force=150.0,
        dt=0.001
    )

    # Factory function has required PSO attributes
    assert hasattr(controller_factory, 'n_gains')         # Number of gains required
    assert hasattr(controller_factory, 'controller_type') # Controller type string
    assert hasattr(controller_factory, 'max_force')       # Force saturation limit

    # Define fitness function using pre-created factory
    def fitness_function(gains_array: np.ndarray) -> float:
        """Fast fitness evaluation using factory function."""

        # Create controller (fast operation)
        controller = controller_factory(gains_array)

        # Evaluate performance
        return evaluate_controller_performance(controller)['total_cost']

    # PSO optimization with optimized factory
    tuner = PSOTuner(
        controller_factory=fitness_function,
        config=config
    )

    return tuner.optimize()