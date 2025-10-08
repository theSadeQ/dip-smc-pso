# Example from: docs\technical\pso_integration_workflows.md
# Index: 25
# Runnable: False
# Hash: 8d1802c0

# example-metadata:
# runnable: false

def robust_pso_optimization(controller_type: ControllerType,
                          max_retries: int = 3) -> Dict[str, Any]:
    """Robust PSO optimization with automatic retry logic."""

    for attempt in range(max_retries):
        try:
            # Adjust configuration based on attempt
            population_size = 20 + (attempt * 5)  # Increase diversity on retries
            max_iterations = 50 + (attempt * 25)   # More patience on retries

            pso_config = PSOFactoryConfig(
                controller_type=controller_type,
                population_size=population_size,
                max_iterations=max_iterations,
                convergence_threshold=1e-5,
                use_robust_evaluation=True,
                fitness_timeout=15.0 + (attempt * 5.0)  # Longer timeout on retries
            )

            pso_factory = EnhancedPSOFactory(pso_config)
            result = pso_factory.optimize_controller()

            if result['success']:
                # Validate result quality
                performance = result['performance_analysis']
                validation = result['validation_results']

                quality_checks = [
                    performance['converged'],
                    validation['gains_valid'],
                    validation['controller_stable'],
                    result['best_cost'] < 1000.0  # Reasonable cost threshold
                ]

                if all(quality_checks):
                    print(f"Optimization successful on attempt {attempt + 1}")
                    return result
                else:
                    print(f"Attempt {attempt + 1}: Poor quality result, retrying...")
                    continue
            else:
                print(f"Attempt {attempt + 1} failed: {result.get('error', 'Unknown')}")
                continue

        except Exception as e:
            print(f"Attempt {attempt + 1} exception: {e}")
            continue

    # All attempts failed
    return {
        'success': False,
        'error': f'Optimization failed after {max_retries} attempts',
        'controller_type': controller_type.value
    }

# Usage
robust_result = robust_pso_optimization(ControllerType.CLASSICAL_SMC, max_retries=3)