# Example from: docs\pso_factory_integration_patterns.md
# Index: 3
# Runnable: True
# Hash: 39ea5dee

from src.controllers.factory import create_all_smc_controllers

def multi_controller_optimization():
    """Optimize gains for multiple controller types simultaneously."""

    # Define gain sets for all controller types
    gains_dict = {
        'classical': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'adaptive': [25.0, 18.0, 15.0, 10.0, 4.0],
        'sta': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
        'hybrid': [18.0, 12.0, 10.0, 8.0]
    }

    # Create all controllers efficiently
    controllers = create_all_smc_controllers(
        gains_dict,
        max_force=150.0,
        dt=0.001
    )

    # Evaluate all controllers
    performance_results = {}
    for controller_type, controller in controllers.items():
        performance_results[controller_type] = evaluate_controller_performance(controller)

    return performance_results

def parallel_multi_objective_pso():
    """Multi-objective PSO across different controller types."""

    controller_types = [SMCType.CLASSICAL, SMCType.ADAPTIVE, SMCType.SUPER_TWISTING]

    # Create factory functions for each type
    factories = {
        ctrl_type: create_pso_controller_factory(ctrl_type)
        for ctrl_type in controller_types
    }

    def multi_objective_fitness(gains_dict: Dict[str, np.ndarray]) -> List[float]:
        """Multi-objective fitness evaluation."""
        objectives = []

        for ctrl_type, gains in gains_dict.items():
            controller = factories[ctrl_type](gains)
            performance = evaluate_controller_performance(controller)
            objectives.append(performance['total_cost'])

        return objectives  # Pareto optimization

    # Run multi-objective PSO
    return run_multi_objective_pso(multi_objective_fitness)