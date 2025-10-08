# Example from: docs\factory\pso_factory_api_reference.md
# Index: 19
# Runnable: True
# Hash: 5b7c5d58

def multi_controller_comparison_example():
    """
    Example demonstrating comparison of all SMC controller types.

    Optimizes all 4 controller types and compares their performance
    across multiple objectives and scenarios.
    """

    # Define test scenarios
    test_scenarios = [
        {
            'name': 'small_disturbance',
            'initial_state': [0.05, 0.05, 0.0, 0.0, 0.0, 0.0],
            'disturbance_amplitude': 2.0
        },
        {
            'name': 'large_disturbance',
            'initial_state': [0.2, 0.15, 0.0, 0.0, 0.0, 0.0],
            'disturbance_amplitude': 10.0
        },
        {
            'name': 'parameter_uncertainty',
            'initial_state': [0.1, 0.1, 0.0, 0.0, 0.0, 0.0],
            'parameter_variations': {'mass_uncertainty': 0.2}
        }
    ]

    # Define optimization objectives
    objectives = {
        'control_performance': {'ise': 0.4, 'overshoot': 0.3, 'settling_time': 0.3},
        'energy_efficiency': {'ise': 0.3, 'control_effort': 0.5, 'chattering': 0.2},
        'robustness': {'ise': 0.2, 'disturbance_rejection': 0.4, 'parameter_sensitivity': 0.4}
    }

    # PSO configuration for all controllers
    base_pso_config = {
        'n_particles': 25,
        'iters': 75,
        'c1': 2.0,
        'c2': 2.0,
        'w': 0.9
    }

    all_results = {}

    # Optimize each controller type
    for smc_type in SMCType:
        print(f"\n{'='*60}")
        print(f"OPTIMIZING {smc_type.value.upper()}")
        print(f"{'='*60}")

        controller_results = {}

        # Test each scenario
        for scenario in test_scenarios:
            print(f"\nScenario: {scenario['name']}")

            scenario_results = {}

            # Test each objective set
            for obj_name, obj_weights in objectives.items():
                print(f"  Objective: {obj_name}")

                # Create simulation config for this scenario
                sim_config = {
                    'duration': 5.0,
                    'dt': 0.01,
                    'initial_state': scenario['initial_state'],
                    'disturbance_amplitude': scenario.get('disturbance_amplitude', 0.0),
                    'parameter_variations': scenario.get('parameter_variations', {}),
                    'objectives': obj_weights
                }

                # Run PSO optimization
                result = optimize_single_controller(
                    smc_type, sim_config, base_pso_config
                )

                scenario_results[obj_name] = result

            controller_results[scenario['name']] = scenario_results

        all_results[smc_type.value] = controller_results

    # Generate comparison analysis
    comparison_analysis = analyze_controller_comparison(all_results, test_scenarios, objectives)

    # Display results
    display_comparison_results(comparison_analysis)

    return comparison_analysis

def optimize_single_controller(smc_type: SMCType,
                              sim_config: Dict[str, Any],
                              pso_config: Dict[str, Any]
                              ) -> Dict[str, Any]:
    """Optimize single controller for given scenario."""

    # Get PSO bounds
    bounds = get_gain_bounds_for_pso(smc_type)
    bounds_array = np.array(bounds)

    # Create fitness function
    def fitness_function(particles: np.ndarray) -> np.ndarray:
        fitness_scores = []

        for gains in particles:
            try:
                controller = create_smc_for_pso(smc_type, gains.tolist())
                result = run_simulation(controller, sim_config)
                fitness = compute_multi_objective_fitness(result, sim_config['objectives'])
                fitness_scores.append(fitness)
            except:
                fitness_scores.append(1000.0)

        return np.array(fitness_scores)

    # Run PSO
    from pyswarms.single import GlobalBestPSO

    optimizer = GlobalBestPSO(
        n_particles=pso_config['n_particles'],
        dimensions=len(bounds),
        options={
            'c1': pso_config['c1'],
            'c2': pso_config['c2'],
            'w': pso_config['w']
        },
        bounds=(bounds_array[:, 0], bounds_array[:, 1])
    )

    best_cost, best_gains = optimizer.optimize(
        fitness_function,
        iters=pso_config['iters'],
        verbose=False
    )

    # Validate result
    final_controller = create_smc_for_pso(smc_type, best_gains.tolist())
    validation_result = run_simulation(final_controller, sim_config)

    return {
        'best_gains': best_gains.tolist(),
        'best_fitness': float(best_cost),
        'validation_metrics': compute_validation_metrics(validation_result),
        'optimization_history': optimizer.cost_history
    }

def analyze_controller_comparison(results: Dict[str, Any],
                                scenarios: List[Dict[str, Any]],
                                objectives: Dict[str, Any]
                                ) -> Dict[str, Any]:
    """Analyze comparison results across controllers."""

    analysis = {
        'overall_ranking': {},
        'scenario_performance': {},
        'objective_performance': {},
        'robustness_analysis': {},
        'recommendations': {}
    }

    # Rank controllers by overall performance
    controller_scores = {}
    for controller_type in results.keys():
        total_score = 0
        count = 0

        for scenario_name in results[controller_type].keys():
            for obj_name in results[controller_type][scenario_name].keys():
                fitness = results[controller_type][scenario_name][obj_name]['best_fitness']
                total_score += fitness
                count += 1

        controller_scores[controller_type] = total_score / count if count > 0 else float('inf')

    # Sort by performance (lower is better)
    analysis['overall_ranking'] = dict(sorted(
        controller_scores.items(), key=lambda x: x[1]
    ))

    # Analyze performance by scenario
    for scenario in scenarios:
        scenario_name = scenario['name']
        scenario_scores = {}

        for controller_type in results.keys():
            if scenario_name in results[controller_type]:
                avg_fitness = np.mean([
                    results[controller_type][scenario_name][obj]['best_fitness']
                    for obj in results[controller_type][scenario_name].keys()
                ])
                scenario_scores[controller_type] = avg_fitness

        analysis['scenario_performance'][scenario_name] = dict(sorted(
            scenario_scores.items(), key=lambda x: x[1]
        ))

    # Analyze performance by objective
    for obj_name in objectives.keys():
        objective_scores = {}

        for controller_type in results.keys():
            obj_scores = []
            for scenario_name in results[controller_type].keys():
                if obj_name in results[controller_type][scenario_name]:
                    obj_scores.append(
                        results[controller_type][scenario_name][obj_name]['best_fitness']
                    )

            if obj_scores:
                objective_scores[controller_type] = np.mean(obj_scores)

        analysis['objective_performance'][obj_name] = dict(sorted(
            objective_scores.items(), key=lambda x: x[1]
        ))

    # Generate recommendations
    analysis['recommendations'] = generate_controller_recommendations(analysis)

    return analysis

def generate_controller_recommendations(analysis: Dict[str, Any]) -> Dict[str, str]:
    """Generate recommendations based on comparison analysis."""

    recommendations = {}

    # Overall best controller
    best_overall = list(analysis['overall_ranking'].keys())[0]
    recommendations['best_overall'] = (
        f"{best_overall} shows the best overall performance across "
        f"all scenarios and objectives."
    )

    # Scenario-specific recommendations
    for scenario, ranking in analysis['scenario_performance'].items():
        best_for_scenario = list(ranking.keys())[0]
        recommendations[f'best_for_{scenario}'] = (
            f"{best_for_scenario} performs best for {scenario} scenarios."
        )

    # Objective-specific recommendations
    for objective, ranking in analysis['objective_performance'].items():
        best_for_objective = list(ranking.keys())[0]
        recommendations[f'best_for_{objective}'] = (
            f"{best_for_objective} excels at {objective} objectives."
        )

    return recommendations

def display_comparison_results(analysis: Dict[str, Any]):
    """Display formatted comparison results."""

    print("\n" + "="*80)
    print("MULTI-CONTROLLER COMPARISON RESULTS")
    print("="*80)

    print("\n🏆 OVERALL RANKING:")
    for i, (controller, score) in enumerate(analysis['overall_ranking'].items(), 1):
        print(f"   {i}. {controller.upper()}: {score:.4f}")

    print("\n📊 SCENARIO PERFORMANCE:")
    for scenario, ranking in analysis['scenario_performance'].items():
        print(f"\n   {scenario.upper()}:")
        for i, (controller, score) in enumerate(ranking.items(), 1):
            print(f"      {i}. {controller}: {score:.4f}")

    print("\n🎯 OBJECTIVE PERFORMANCE:")
    for objective, ranking in analysis['objective_performance'].items():
        print(f"\n   {objective.upper()}:")
        for i, (controller, score) in enumerate(ranking.items(), 1):
            print(f"      {i}. {controller}: {score:.4f}")

    print("\n💡 RECOMMENDATIONS:")
    for key, recommendation in analysis['recommendations'].items():
        print(f"   • {recommendation}")

    print("\n" + "="*80)

# Run the comparison example
if __name__ == "__main__":
    comparison_results = multi_controller_comparison_example()