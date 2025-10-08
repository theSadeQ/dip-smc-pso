# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 4
# Runnable: False
# Hash: a4acd9c2

def multi_objective_pso_optimization(
    controller_types: List[str],
    simulation_config: Any,
    objectives: Dict[str, float],  # {'ise': 0.4, 'overshoot': 0.3, 'energy': 0.3}
    pso_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Multi-objective PSO optimization across multiple controller types.

    Features:
    - Simultaneous optimization of multiple performance metrics
    - Pareto-optimal solution discovery
    - Controller comparison and ranking
    - Robust constraint handling
    """

    results = {}
    pareto_solutions = []

    for controller_type in controller_types:
        print(f"Optimizing {controller_type}...")

        # Single-objective optimization for baseline
        single_result = optimize_smc_controller_pso(
            controller_type, simulation_config, pso_config,
            list(objectives.keys())
        )

        results[controller_type] = single_result

        # Extract Pareto solutions
        pareto_solutions.extend(
            extract_pareto_solutions(single_result, objectives)
        )

    # Multi-objective analysis
    pareto_front = compute_pareto_front(pareto_solutions)
    controller_ranking = rank_controllers_by_objectives(results, objectives)

    return {
        'individual_results': results,
        'pareto_front': pareto_front,
        'controller_ranking': controller_ranking,
        'best_overall': select_best_overall_solution(results, objectives)
    }