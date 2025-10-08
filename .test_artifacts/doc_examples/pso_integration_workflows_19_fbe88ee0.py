# Example from: docs\technical\pso_integration_workflows.md
# Index: 19
# Runnable: True
# Hash: fbe88ee0

def production_optimization_pipeline(controller_type: str,
                                   config_path: str = "config.yaml",
                                   output_path: str = "optimized_gains.json"):
    """Production-ready PSO optimization pipeline."""

    import json
    import logging
    from datetime import datetime

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Map string to enum
    controller_type_map = {
        'classical_smc': ControllerType.CLASSICAL_SMC,
        'sta_smc': ControllerType.STA_SMC,
        'adaptive_smc': ControllerType.ADAPTIVE_SMC,
        'hybrid_adaptive_sta_smc': ControllerType.HYBRID_SMC
    }

    if controller_type not in controller_type_map:
        raise ValueError(f"Unknown controller type: {controller_type}")

    controller_enum = controller_type_map[controller_type]

    try:
        # Production PSO configuration
        pso_config = PSOFactoryConfig(
            controller_type=controller_enum,
            population_size=25,              # Balanced exploration/exploitation
            max_iterations=100,              # Sufficient for convergence
            convergence_threshold=1e-6,      # High precision
            max_stagnation_iterations=15,    # Prevent premature termination
            enable_adaptive_bounds=True,     # Dynamic optimization
            fitness_timeout=20.0,           # Generous timeout
            use_robust_evaluation=True      # Production reliability
        )

        logger.info(f"Starting production optimization for {controller_type}")
        logger.info(f"Configuration: {pso_config}")

        # Create factory and optimize
        pso_factory = EnhancedPSOFactory(pso_config, config_path)

        start_time = datetime.now()
        optimization_result = pso_factory.optimize_controller()
        end_time = datetime.now()

        optimization_time = (end_time - start_time).total_seconds()

        if optimization_result['success']:
            # Extract optimized parameters
            best_gains = optimization_result['best_gains']
            best_cost = optimization_result['best_cost']

            # Validation results
            validation = optimization_result['validation_results']
            performance = optimization_result['performance_analysis']

            # Production validation checks
            production_ready = (
                validation['gains_valid'] and
                validation['controller_stable'] and
                validation['performance_acceptable'] and
                performance['converged']
            )

            # Prepare production data
            production_data = {
                'controller_type': controller_type,
                'optimization_timestamp': start_time.isoformat(),
                'optimization_duration_seconds': optimization_time,
                'optimized_gains': best_gains,
                'optimization_cost': best_cost,
                'convergence_analysis': performance,
                'validation_results': validation,
                'production_ready': production_ready,
                'optimization_configuration': {
                    'population_size': pso_config.population_size,
                    'max_iterations': pso_config.max_iterations,
                    'convergence_threshold': pso_config.convergence_threshold
                }
            }

            # Save results
            with open(output_path, 'w') as f:
                json.dump(production_data, f, indent=2)

            logger.info(f"Optimization completed successfully")
            logger.info(f"Best cost: {best_cost:.6f}")
            logger.info(f"Optimized gains: {best_gains}")
            logger.info(f"Production ready: {production_ready}")
            logger.info(f"Results saved to: {output_path}")

            if not production_ready:
                logger.warning("Controller may not be production ready - review validation results")

            return optimization_result

        else:
            error_msg = optimization_result.get('error', 'Unknown error')
            logger.error(f"Optimization failed: {error_msg}")

            # Save failure information
            failure_data = {
                'controller_type': controller_type,
                'optimization_timestamp': start_time.isoformat(),
                'optimization_duration_seconds': optimization_time,
                'status': 'FAILED',
                'error': error_msg,
                'optimization_stats': optimization_result.get('optimization_stats', {})
            }

            failure_path = output_path.replace('.json', '_failure.json')
            with open(failure_path, 'w') as f:
                json.dump(failure_data, f, indent=2)

            logger.info(f"Failure data saved to: {failure_path}")

            return None

    except Exception as e:
        logger.error(f"Production optimization pipeline failed: {e}")
        raise

# Usage examples
classical_result = production_optimization_pipeline('classical_smc', output_path='classical_gains.json')
sta_result = production_optimization_pipeline('sta_smc', output_path='sta_gains.json')
adaptive_result = production_optimization_pipeline('adaptive_smc', output_path='adaptive_gains.json')