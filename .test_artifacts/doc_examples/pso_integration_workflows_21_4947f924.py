# Example from: docs\technical\pso_integration_workflows.md
# Index: 21
# Runnable: False
# Hash: 4947f924

# example-metadata:
# runnable: false

def complete_research_workflow():
    """Complete research workflow demonstrating PSO-factory integration."""

    print("=== Complete Research Workflow ===")

    # Step 1: Baseline controllers
    print("\n1. Creating baseline controllers...")

    from src.controllers.factory import create_controller

    baseline_controllers = {
        'classical': create_controller('classical_smc', gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]),
        'sta': create_controller('sta_smc', gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43]),
        'adaptive': create_controller('adaptive_smc', gains=[12.0, 10.0, 6.0, 5.0, 2.5])
    }

    print(f"Created {len(baseline_controllers)} baseline controllers")

    # Step 2: PSO optimization
    print("\n2. Running PSO optimization...")

    optimization_results = {}

    for controller_name in ['classical_smc', 'sta_smc', 'adaptive_smc']:
        controller_enum = {
            'classical_smc': ControllerType.CLASSICAL_SMC,
            'sta_smc': ControllerType.STA_SMC,
            'adaptive_smc': ControllerType.ADAPTIVE_SMC
        }[controller_name]

        pso_config = PSOFactoryConfig(
            controller_type=controller_enum,
            population_size=20,
            max_iterations=60,
            use_robust_evaluation=True
        )

        pso_factory = EnhancedPSOFactory(pso_config)
        result = pso_factory.optimize_controller()

        optimization_results[controller_name] = result

        if result['success']:
            cost = result['best_cost']
            converged = result['performance_analysis']['converged']
            print(f"  {controller_name}: cost={cost:.6f}, converged={converged}")
        else:
            print(f"  {controller_name}: FAILED - {result.get('error', 'Unknown')}")

    # Step 3: Performance comparison
    print("\n3. Performance comparison...")

    comparison_data = []

    for controller_name, result in optimization_results.items():
        if result['success']:
            comparison_data.append({
                'controller': controller_name,
                'cost': result['best_cost'],
                'gains': result['best_gains'],
                'converged': result['performance_analysis']['converged'],
                'improvement': result['performance_analysis']['improvement_ratio']
            })

    # Sort by cost (lower is better)
    comparison_data.sort(key=lambda x: x['cost'])

    print(f"{'Rank':<4} {'Controller':<15} {'Cost':<12} {'Converged':<10} {'Improvement':<12}")
    print("-" * 55)

    for i, data in enumerate(comparison_data, 1):
        print(f"{i:<4} {data['controller']:<15} {data['cost']:<12.6f} "
              f"{str(data['converged']):<10} {data['improvement']:<12.1%}")

    # Step 4: Best controller analysis
    if comparison_data:
        best_controller = comparison_data[0]
        print(f"\n4. Best controller analysis:")
        print(f"  Controller: {best_controller['controller']}")
        print(f"  Cost: {best_controller['cost']:.6f}")
        print(f"  Gains: {best_controller['gains']}")
        print(f"  Converged: {best_controller['converged']}")
        print(f"  Improvement: {best_controller['improvement']:.1%}")

        # Create optimized controller
        best_name = best_controller['controller']
        best_gains = best_controller['gains']

        optimized_controller = create_controller(best_name, gains=best_gains)

        print(f"  Optimized controller ready for deployment")

        return {
            'baseline_controllers': baseline_controllers,
            'optimization_results': optimization_results,
            'best_controller': optimized_controller,
            'comparison_data': comparison_data
        }

    else:
        print("No successful optimizations")
        return None

# Run complete workflow
workflow_results = complete_research_workflow()