# Example from: docs\technical\pso_integration_workflows.md
# Index: 26
# Runnable: True
# Hash: 83c1a92b

def performance_optimized_workflow(controller_types: List[ControllerType],
                                 parallel_execution: bool = True) -> Dict[str, Any]:
    """Performance-optimized PSO workflow."""

    import concurrent.futures
    import multiprocessing

    def optimize_with_caching(controller_type: ControllerType) -> Tuple[ControllerType, Dict]:
        """Optimize with result caching."""

        # Check for cached results
        cache_key = f"{controller_type.value}_optimized"

        # Configure for performance
        pso_config = PSOFactoryConfig(
            controller_type=controller_type,
            population_size=20,        # Balanced size
            max_iterations=60,         # Reasonable iterations
            convergence_threshold=1e-5, # Good precision
            fitness_timeout=10.0,      # Efficient timeout
            use_robust_evaluation=True
        )

        pso_factory = EnhancedPSOFactory(pso_config)
        result = pso_factory.optimize_controller()

        return controller_type, result

    results = {}

    if parallel_execution and len(controller_types) > 1:
        # Parallel execution
        max_workers = min(len(controller_types), multiprocessing.cpu_count())

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_type = {
                executor.submit(optimize_with_caching, ct): ct
                for ct in controller_types
            }

            for future in concurrent.futures.as_completed(future_to_type):
                controller_type, result = future.result()
                results[controller_type.value] = result
    else:
        # Sequential execution
        for controller_type in controller_types:
            controller_type_result, result = optimize_with_caching(controller_type)
            results[controller_type.value] = result

    return results

# Usage
controller_types = [ControllerType.CLASSICAL_SMC, ControllerType.STA_SMC, ControllerType.ADAPTIVE_SMC]
performance_results = performance_optimized_workflow(controller_types, parallel_execution=True)