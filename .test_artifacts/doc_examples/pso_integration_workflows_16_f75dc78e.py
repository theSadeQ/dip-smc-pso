# Example from: docs\technical\pso_integration_workflows.md
# Index: 16
# Runnable: False
# Hash: f75dc78e

# example-metadata:
# runnable: false

def comprehensive_diagnostics(pso_factory, optimization_result):
    """Generate comprehensive optimization diagnostics."""

    print("=== Comprehensive PSO Diagnostics ===")

    # 1. Configuration summary
    diagnostics = pso_factory.get_optimization_diagnostics()
    config = diagnostics['configuration']

    print(f"\nConfiguration:")
    print(f"  Controller type: {config['controller_type']}")
    print(f"  Population size: {config['population_size']}")
    print(f"  Max iterations: {config['max_iterations']}")
    print(f"  Convergence threshold: {config['convergence_threshold']}")

    # 2. Controller specifications
    specs = diagnostics['controller_specs']
    print(f"\nController Specifications:")
    print(f"  Expected gains: {specs['n_gains']}")
    print(f"  Bounds: {specs['bounds']}")
    print(f"  Default gains: {specs['default_gains']}")

    # 3. Validation statistics
    stats = diagnostics['validation_statistics']
    print(f"\nValidation Statistics:")
    print(f"  Fitness evaluations: {stats['fitness_evaluations']}")
    print(f"  Failed evaluations: {stats['failed_evaluations']}")
    print(f"  Parameter violations: {stats['parameter_violations']}")

    # 4. Optimization outcome
    if optimization_result['success']:
        print(f"\nOptimization Outcome:")
        print(f"  Status: SUCCESS")
        print(f"  Best cost: {optimization_result['best_cost']:.6f}")
        print(f"  Best gains: {optimization_result['best_gains']}")

        # Performance analysis
        perf = optimization_result['performance_analysis']
        print(f"  Converged: {perf['converged']}")
        print(f"  Improvement: {perf['improvement_ratio']:.1%}")

        # Validation results
        validation = optimization_result['validation_results']
        print(f"  Gains valid: {validation['gains_valid']}")
        print(f"  Controller stable: {validation['controller_stable']}")

    else:
        print(f"\nOptimization Outcome:")
        print(f"  Status: FAILED")
        print(f"  Error: {optimization_result.get('error', 'Unknown')}")

# Usage example
pso_factory = EnhancedPSOFactory(pso_config)
result = pso_factory.optimize_controller()
comprehensive_diagnostics(pso_factory, result)