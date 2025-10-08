# Example from: docs\pso_factory_integration_patterns.md
# Index: 11
# Runnable: True
# Hash: 8b3eb923

def multi_objective_pso_optimization(controller_type: SMCType) -> Dict[str, Any]:
    """Multi-objective PSO optimization for SMC controllers."""

    # Define multiple objectives
    objectives = {
        'tracking_performance': lambda controller: evaluate_tracking_error(controller),
        'control_efficiency': lambda controller: evaluate_control_effort(controller),
        'robustness': lambda controller: evaluate_robustness_index(controller),
        'chattering_minimization': lambda controller: evaluate_chattering_index(controller)
    }

    # Create controller factory
    factory = create_pso_controller_factory(controller_type)

    # Multi-objective fitness function
    def multi_objective_fitness(gains: np.ndarray) -> List[float]:
        """Evaluate multiple objectives."""
        try:
            controller = factory(gains)
            return [objective_func(controller) for objective_func in objectives.values()]
        except:
            return [float('inf')] * len(objectives)

    # Pareto optimization using NSGA-II-style PSO
    from src.optimization.algorithms.multi_objective_pso import MultiObjectivePSO

    optimizer = MultiObjectivePSO(
        fitness_function=multi_objective_fitness,
        n_objectives=len(objectives),
        n_particles=100,
        n_dimensions=factory.n_gains,
        bounds=get_gain_bounds_for_pso(controller_type),
        max_iterations=200
    )

    pareto_solutions = optimizer.optimize()

    # Analyze Pareto front
    pareto_analysis = {
        'n_solutions': len(pareto_solutions),
        'objective_ranges': analyze_objective_ranges(pareto_solutions),
        'recommended_solution': select_best_tradeoff_solution(pareto_solutions),
        'diversity_metric': compute_pareto_diversity(pareto_solutions)
    }

    return {
        'pareto_solutions': pareto_solutions,
        'analysis': pareto_analysis,
        'objective_names': list(objectives.keys())
    }