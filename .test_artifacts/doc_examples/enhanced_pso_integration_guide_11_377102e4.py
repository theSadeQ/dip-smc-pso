# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 11
# Runnable: True
# Hash: 377102e4

def robust_pso_optimization(
    controller_type: str,
    simulation_config: Any,
    pso_config: Dict[str, Any],
    error_handling_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Production-ready PSO optimization with comprehensive error handling.

    Features:
    - Graceful degradation for simulation failures
    - Automatic retry mechanisms
    - Fallback strategies for numerical instabilities
    - Comprehensive logging and diagnostics
    """

    import logging
    import traceback
    from contextlib import contextmanager

    # Setup logging
    logger = logging.getLogger('PSO_Optimization')

    @contextmanager
    def error_context(operation_name: str):
        """Context manager for operation-specific error handling."""
        try:
            logger.info(f"Starting {operation_name}")
            yield
            logger.info(f"Completed {operation_name}")
        except Exception as e:
            logger.error(f"Error in {operation_name}: {e}")
            logger.debug(traceback.format_exc())
            raise

    try:
        with error_context("PSO Initialization"):
            # Initialize with validation
            pso_interface = PSOFactoryInterface(controller_type, simulation_config)

            # Validate PSO configuration
            validate_pso_configuration(pso_config, pso_interface.n_gains)

        with error_context("Fitness Function Setup"):
            # Create robust fitness function with fallbacks
            fitness_function = create_robust_fitness_function(
                pso_interface, simulation_config, error_handling_config
            )

        with error_context("PSO Execution"):
            # Run PSO with monitoring
            result = run_monitored_pso_optimization(
                fitness_function, pso_config, error_handling_config
            )

        with error_context("Result Validation"):
            # Validate optimization results
            validated_result = validate_and_refine_result(
                result, controller_type, simulation_config
            )

        return validated_result

    except Exception as e:
        logger.error(f"PSO optimization failed: {e}")

        # Attempt fallback optimization
        if error_handling_config.get('enable_fallback', True):
            logger.info("Attempting fallback optimization")
            return fallback_optimization_strategy(
                controller_type, simulation_config, pso_config
            )
        else:
            raise

def create_robust_fitness_function(
    pso_interface: PSOFactoryInterface,
    simulation_config: Any,
    error_config: Dict[str, Any]
) -> Callable:
    """Create fitness function with comprehensive error handling."""

    max_retries = error_config.get('max_retries', 3)
    timeout = error_config.get('simulation_timeout', 30.0)

    def robust_fitness(particles: np.ndarray) -> np.ndarray:
        """Robust fitness evaluation with retries and timeouts."""

        fitness_scores = []

        for particle in particles:
            best_score = float('inf')

            for retry in range(max_retries):
                try:
                    # Create controller with timeout
                    with timeout_context(timeout):
                        controller = pso_interface.create_controller(particle)

                        # Run simulation with monitoring
                        result = run_monitored_simulation(controller, simulation_config)

                        # Compute fitness
                        score = compute_robust_fitness(result, error_config)

                        best_score = min(best_score, score)
                        break  # Success, no need to retry

                except TimeoutError:
                    logger.warning(f"Simulation timeout for particle {particle}")
                    continue
                except Exception as e:
                    logger.warning(f"Simulation error (retry {retry}): {e}")
                    continue

            fitness_scores.append(best_score)

        return np.array(fitness_scores)

    return robust_fitness