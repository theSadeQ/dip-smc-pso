# Example from: docs\technical\pso_integration_workflows.md
# Index: 20
# Runnable: False
# Hash: 30bc08bc

# example-metadata:
# runnable: false

def batch_optimization_workflow(controller_types: List[str],
                              optimization_configs: Dict[str, Dict] = None):
    """Batch optimization workflow for multiple controllers."""

    import concurrent.futures
    import os
    from datetime import datetime

    if optimization_configs is None:
        optimization_configs = {}

    def optimize_single_controller(controller_type):
        """Optimize a single controller type."""
        try:
            # Get custom config or use defaults
            custom_config = optimization_configs.get(controller_type, {})

            # Default configuration
            default_config = {
                'population_size': 25,
                'max_iterations': 75,
                'convergence_threshold': 1e-6,
                'enable_adaptive_bounds': True,
                'use_robust_evaluation': True
            }

            # Merge configurations
            config_params = {**default_config, **custom_config}

            controller_enum = {
                'classical_smc': ControllerType.CLASSICAL_SMC,
                'sta_smc': ControllerType.STA_SMC,
                'adaptive_smc': ControllerType.ADAPTIVE_SMC,
                'hybrid_adaptive_sta_smc': ControllerType.HYBRID_SMC
            }[controller_type]

            pso_config = PSOFactoryConfig(
                controller_type=controller_enum,
                **config_params
            )

            pso_factory = EnhancedPSOFactory(pso_config)
            result = pso_factory.optimize_controller()

            return controller_type, result

        except Exception as e:
            return controller_type, {'success': False, 'error': str(e)}

    # Parallel optimization
    print(f"Starting batch optimization for {len(controller_types)} controllers...")

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit optimization tasks
        future_to_controller = {
            executor.submit(optimize_single_controller, ct): ct
            for ct in controller_types
        }

        # Collect results
        for future in concurrent.futures.as_completed(future_to_controller):
            controller_type = future_to_controller[future]
            try:
                controller_name, optimization_result = future.result()
                results[controller_name] = optimization_result

                if optimization_result['success']:
                    cost = optimization_result['best_cost']
                    print(f"✅ {controller_name}: {cost:.6f}")
                else:
                    error = optimization_result.get('error', 'Unknown')
                    print(f"❌ {controller_name}: {error}")

            except Exception as e:
                print(f"❌ {controller_type}: Exception - {e}")
                results[controller_type] = {'success': False, 'error': str(e)}

    # Save batch results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_results_path = f"batch_optimization_{timestamp}.json"

    with open(batch_results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nBatch optimization completed. Results saved to: {batch_results_path}")

    # Summary report
    successful = sum(1 for r in results.values() if r['success'])
    total = len(results)

    print(f"\nBatch Summary:")
    print(f"  Total controllers: {total}")
    print(f"  Successful optimizations: {successful}")
    print(f"  Failed optimizations: {total - successful}")
    print(f"  Success rate: {successful/total:.1%}")

    return results

# Usage example
controllers_to_optimize = ['classical_smc', 'sta_smc', 'adaptive_smc']

# Custom configurations for specific controllers
custom_configs = {
    'sta_smc': {
        'population_size': 30,      # Larger population for STA-SMC
        'max_iterations': 100,      # More iterations for Issue #2 resolution
        'convergence_threshold': 1e-5
    },
    'adaptive_smc': {
        'population_size': 35,      # Complex parameter space
        'max_iterations': 120
    }
}

batch_results = batch_optimization_workflow(controllers_to_optimize, custom_configs)