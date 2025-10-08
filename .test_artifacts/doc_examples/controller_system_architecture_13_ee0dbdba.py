# Example from: docs\architecture\controller_system_architecture.md
# Index: 13
# Runnable: False
# Hash: ee0dbdba

def pso_optimization_data_flow():
    """
    Data flow through PSO optimization process.

    1. Parameter Bounds → Swarm Initialization
    2. Swarm Positions → Controller Instances
    3. Controller Performance → Fitness Evaluation
    4. Fitness Values → Swarm Updates
    5. Convergence Check → Result Extraction
    """

    # Step 1: Swarm Initialization
    parameter_bounds = get_controller_bounds(controller_type)
    swarm_positions = initialize_swarm(n_particles, parameter_bounds)

    # Step 2: Parallel Fitness Evaluation
    fitness_results = []
    for particle_position in swarm_positions:
        # Create controller with candidate parameters
        candidate_controller = create_controller(controller_type, gains=particle_position)

        # Evaluate performance
        simulation_result = run_simulation(candidate_controller)
        fitness_score = compute_fitness(simulation_result)
        fitness_results.append(fitness_score)

    # Step 3: Swarm Update
    updated_swarm = update_swarm_velocities_and_positions(
        swarm_positions,
        fitness_results,
        global_best,
        personal_bests
    )

    # Step 4: Convergence Analysis
    convergence_status = analyze_convergence(fitness_results, convergence_criteria)

    # Step 5: Result Packaging
    optimization_result = OptimizationResult(
        best_gains=global_best.position,
        best_cost=global_best.fitness,
        convergence_iterations=current_iteration,
        convergence_status=convergence_status
    )

    return optimization_result