# Example from: docs\technical\pso_integration_workflows.md
# Index: 18
# Runnable: False
# Hash: 4f83074d

def compare_controller_performance():
    """Compare optimized controllers across different types."""

    # Optimize all controller types
    controller_types = [
        ControllerType.CLASSICAL_SMC,
        ControllerType.STA_SMC,
        ControllerType.ADAPTIVE_SMC
    ]

    results = {}

    for controller_type in controller_types:
        print(f"Optimizing {controller_type.value}...")

        pso_config = PSOFactoryConfig(
            controller_type=controller_type,
            population_size=20,
            max_iterations=50
        )

        pso_factory = EnhancedPSOFactory(pso_config)
        result = pso_factory.optimize_controller()

        results[controller_type.value] = result

    # Performance comparison
    print("\n=== Controller Performance Comparison ===")
    print(f"{'Controller':<20} {'Best Cost':<12} {'Converged':<10} {'Improvement':<12}")
    print("-" * 60)

    for controller_name, result in results.items():
        if result['success']:
            best_cost = result['best_cost']
            converged = result['performance_analysis']['converged']
            improvement = result['performance_analysis']['improvement_ratio']

            print(f"{controller_name:<20} {best_cost:<12.6f} {str(converged):<10} {improvement:<12.1%}")
        else:
            print(f"{controller_name:<20} {'FAILED':<12} {'-':<10} {'-':<12}")

    return results

# Run comparison
comparison_results = compare_controller_performance()