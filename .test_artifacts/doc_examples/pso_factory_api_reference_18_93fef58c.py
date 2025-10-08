# Example from: docs\factory\pso_factory_api_reference.md
# Index: 18
# Runnable: False
# Hash: 93fef58c

def complete_pso_optimization_example():
    """
    Complete example demonstrating PSO-Factory integration.

    This example shows:
    1. Configuration setup
    2. Controller creation and validation
    3. PSO optimization execution
    4. Performance monitoring
    5. Results analysis and validation
    """

    # Step 1: Configuration setup
    pso_config = PSOFactoryConfig(
        controller_type=SMCType.CLASSICAL,
        max_force=100.0,
        dt=0.01,
        pso_params={
            'n_particles': 30,
            'iters': 100,
            'c1': 2.0,
            'c2': 2.0,
            'w': 0.9
        },
        enable_monitoring=True,
        strict_validation=True
    )

    # Step 2: Simulation configuration
    simulation_config = {
        'duration': 5.0,
        'dt': 0.01,
        'initial_state': [0.1, 0.1, 0.0, 0.0, 0.0, 0.0],  # Small perturbation
        'disturbances': {
            'enable': True,
            'amplitude': 5.0,
            'frequency': 1.0
        },
        'performance_objectives': ['ise', 'overshoot', 'control_effort']
    }

    # Step 3: PSO optimization with monitoring
    with monitor_pso_performance(pso_config.pso_params) as monitor:

        # Define fitness function
        @handle_pso_errors
        def fitness_function(particles: np.ndarray) -> np.ndarray:
            fitness_scores = []

            for gains in particles:
                start_time = time.perf_counter()

                try:
                    # Create controller with validation
                    controller = create_smc_for_pso(
                        pso_config.controller_type,
                        gains.tolist(),
                        pso_config.max_force
                    )
                    creation_time = time.perf_counter() - start_time
                    monitor.log_controller_creation(True, creation_time)

                    # Run simulation
                    sim_start = time.perf_counter()
                    result = run_simulation(controller, simulation_config)
                    sim_time = time.perf_counter() - sim_start
                    monitor.log_simulation_execution(True, sim_time)

                    # Compute fitness
                    fitness_start = time.perf_counter()
                    fitness = compute_multi_objective_fitness(
                        result, simulation_config['performance_objectives']
                    )
                    fitness_time = time.perf_counter() - fitness_start
                    monitor.log_fitness_evaluation(fitness, fitness_time)

                    fitness_scores.append(fitness)

                except Exception as e:
                    monitor.log_controller_creation(False, 0.0)
                    fitness_scores.append(1000.0)

                # Log resource usage periodically
                if len(fitness_scores) % 10 == 0:
                    monitor.log_resource_usage()

            return np.array(fitness_scores)

        # Step 4: Execute PSO optimization
        from pyswarms.single import GlobalBestPSO

        bounds = pso_config.gain_bounds
        bounds_array = np.array(bounds)

        optimizer = GlobalBestPSO(
            n_particles=pso_config.pso_params['n_particles'],
            dimensions=pso_config.n_gains,
            options={
                'c1': pso_config.pso_params['c1'],
                'c2': pso_config.pso_params['c2'],
                'w': pso_config.pso_params['w']
            },
            bounds=(bounds_array[:, 0], bounds_array[:, 1])
        )

        print("Starting PSO optimization...")
        best_cost, best_gains = optimizer.optimize(
            fitness_function,
            iters=pso_config.pso_params['iters'],
            verbose=True
        )

    # Step 5: Results analysis
    performance_report = monitor.generate_performance_report()

    # Validate optimized controller
    optimized_controller = create_smc_for_pso(
        pso_config.controller_type,
        best_gains.tolist(),
        pso_config.max_force
    )

    # Run validation simulation
    validation_result = run_simulation(optimized_controller, simulation_config)
    validation_metrics = compute_validation_metrics(validation_result)

    # Step 6: Generate comprehensive report
    optimization_report = {
        'optimization_results': {
            'best_gains': best_gains.tolist(),
            'best_fitness': float(best_cost),
            'optimization_history': optimizer.cost_history,
            'convergence_iteration': find_convergence_iteration(optimizer.cost_history)
        },
        'validation_results': {
            'controller_gains': optimized_controller.gains,
            'performance_metrics': validation_metrics,
            'stability_analysis': estimate_stability_properties(
                pso_config.controller_type, best_gains.tolist()
            )
        },
        'performance_report': performance_report,
        'configuration': {
            'pso_config': pso_config.__dict__,
            'simulation_config': simulation_config,
            'bounds_used': bounds
        }
    }

    # Step 7: Display results
    print_optimization_summary(optimization_report)

    return optimization_report

def print_optimization_summary(report: Dict[str, Any]):
    """Print formatted optimization summary."""

    opt_results = report['optimization_results']
    val_results = report['validation_results']
    perf_report = report['performance_report']

    print("\n" + "="*80)
    print("PSO OPTIMIZATION RESULTS SUMMARY")
    print("="*80)

    print(f"\n📊 OPTIMIZATION RESULTS:")
    print(f"   Best Fitness: {opt_results['best_fitness']:.6f}")
    print(f"   Best Gains: {opt_results['best_gains']}")
    print(f"   Convergence: Iteration {opt_results['convergence_iteration']}")

    print(f"\n🎯 VALIDATION METRICS:")
    for metric, value in val_results['performance_metrics'].items():
        print(f"   {metric.upper()}: {value:.4f}")

    print(f"\n⚡ PERFORMANCE SUMMARY:")
    summary = perf_report['summary']
    print(f"   Total Evaluations: {summary['total_evaluations']}")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")
    print(f"   Evaluations/sec: {summary['evaluations_per_second']:.1f}")
    print(f"   Total Time: {summary['total_optimization_time']:.1f}s")

    perf = perf_report['performance']
    print(f"   Avg Creation Time: {perf['average_controller_creation_time_ms']:.2f}ms")
    print(f"   Avg Simulation Time: {perf['average_simulation_time_ms']:.2f}ms")

    resources = perf_report['resources']
    print(f"   Peak Memory: {resources['peak_memory_usage_percent']:.1f}%")
    print(f"   Avg CPU: {resources['average_cpu_utilization_percent']:.1f}%")

    if perf_report['alerts']:
        print(f"\n⚠️  PERFORMANCE ALERTS:")
        for alert in perf_report['alerts']:
            print(f"   - {alert}")

    print("\n" + "="*80)

def find_convergence_iteration(cost_history: List[float],
                              tolerance: float = 1e-6,
                              patience: int = 10
                              ) -> int:
    """Find iteration where PSO converged."""

    if len(cost_history) < patience:
        return len(cost_history)

    for i in range(patience, len(cost_history)):
        # Check if fitness has been stable for 'patience' iterations
        recent_costs = cost_history[i-patience:i]
        if max(recent_costs) - min(recent_costs) < tolerance:
            return i - patience + 1

    return len(cost_history)  # No convergence detected

# Run the complete example
if __name__ == "__main__":
    optimization_report = complete_pso_optimization_example()