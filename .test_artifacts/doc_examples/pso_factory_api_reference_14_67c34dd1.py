# Example from: docs\factory\pso_factory_api_reference.md
# Index: 14
# Runnable: False
# Hash: 67c34dd1

def multi_objective_pso_optimization(
    controller_types: List[SMCType],
    simulation_config: Dict[str, Any],
    objectives: Dict[str, float],
    pso_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Multi-objective PSO optimization across multiple controller types.

    Optimizes multiple SMC controllers simultaneously using weighted
    multi-objective fitness functions with Pareto front analysis.

    Args:
        controller_types: List of SMC types to optimize
        simulation_config: Simulation parameters
        objectives: Objective weights {'ise': 0.4, 'overshoot': 0.3, 'energy': 0.3}
        pso_config: PSO algorithm configuration

    Returns:
        Comprehensive optimization results with Pareto analysis
    """

    results = {}
    all_solutions = []

    for smc_type in controller_types:
        print(f"Optimizing {smc_type.value}...")

        # Get PSO bounds for this controller type
        bounds = get_gain_bounds_for_pso(smc_type)

        # Create multi-objective fitness function
        def multi_objective_fitness(particles: np.ndarray) -> np.ndarray:
            fitness_scores = []

            for gains in particles:
                try:
                    # Create controller with validation
                    controller = create_smc_for_pso(smc_type, gains.tolist())

                    # Run simulation
                    sim_result = run_simulation(controller, simulation_config)

                    # Compute individual objectives
                    ise = compute_ise(sim_result)
                    overshoot = compute_overshoot(sim_result)
                    energy = compute_control_energy(sim_result)

                    # Weighted combination
                    fitness = (objectives.get('ise', 0.0) * ise +
                             objectives.get('overshoot', 0.0) * overshoot +
                             objectives.get('energy', 0.0) * energy)

                    fitness_scores.append(fitness)

                    # Store solution for Pareto analysis
                    all_solutions.append({
                        'controller_type': smc_type,
                        'gains': gains.tolist(),
                        'fitness': fitness,
                        'objectives': {'ise': ise, 'overshoot': overshoot, 'energy': energy}
                    })

                except Exception:
                    fitness_scores.append(1000.0)

            return np.array(fitness_scores)

        # Run PSO optimization
        from pyswarms.single import GlobalBestPSO
        bounds_array = np.array(bounds)

        optimizer = GlobalBestPSO(
            n_particles=pso_config.get('n_particles', 30),
            dimensions=len(bounds),
            options={
                'c1': pso_config.get('c1', 2.0),
                'c2': pso_config.get('c2', 2.0),
                'w': pso_config.get('w', 0.9)
            },
            bounds=(bounds_array[:, 0], bounds_array[:, 1])
        )

        best_cost, best_gains = optimizer.optimize(
            multi_objective_fitness,
            iters=pso_config.get('iters', 100)
        )

        results[smc_type.value] = {
            'best_gains': best_gains.tolist(),
            'best_fitness': float(best_cost),
            'optimization_history': optimizer.cost_history
        }

    # Pareto front analysis
    pareto_front = compute_pareto_front(all_solutions, objectives)
    controller_ranking = rank_controllers_by_objectives(results, objectives)

    return {
        'individual_results': results,
        'pareto_front': pareto_front,
        'controller_ranking': controller_ranking,
        'best_overall': select_best_overall_solution(results, objectives)
    }

def compute_pareto_front(solutions: List[Dict[str, Any]],
                        objectives: Dict[str, float]
                        ) -> List[Dict[str, Any]]:
    """
    Compute Pareto-optimal solutions from multi-objective optimization.

    Args:
        solutions: List of solution dictionaries
        objectives: Objective weights

    Returns:
        List of Pareto-optimal solutions
    """
    pareto_solutions = []

    for i, solution_i in enumerate(solutions):
        is_dominated = False

        for j, solution_j in enumerate(solutions):
            if i == j:
                continue

            # Check if solution_j dominates solution_i
            obj_i = solution_i['objectives']
            obj_j = solution_j['objectives']

            dominates = True
            for obj_name in objectives.keys():
                if obj_j[obj_name] >= obj_i[obj_name]:  # j is not better in this objective
                    dominates = False
                    break

            if dominates:
                is_dominated = True
                break

        if not is_dominated:
            pareto_solutions.append(solution_i)

    return pareto_solutions