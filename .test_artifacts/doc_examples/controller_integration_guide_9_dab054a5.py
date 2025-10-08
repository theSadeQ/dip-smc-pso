# Example from: docs\factory\controller_integration_guide.md
# Index: 9
# Runnable: False
# Hash: dab054a5

# example-metadata:
# runnable: false

def create_pso_optimized_controller(
    controller_type: str,
    gains: GainsArray,
    plant_config: Any,
    pso_options: Optional[Dict[str, Any]] = None
) -> PSOControllerWrapper:
    """
    Create PSO-optimized controller with comprehensive integration.

    Args:
        controller_type: Type of SMC controller
        gains: Controller gains for optimization
        plant_config: Plant configuration
        pso_options: PSO-specific options

    Returns:
        PSO-wrapped controller ready for optimization
    """

    # Default PSO options
    default_pso_options = {
        'validation_enabled': True,
        'performance_monitoring': True,
        'safety_limits': True,
        'real_time_constraints': True
    }

    if pso_options:
        default_pso_options.update(pso_options)

    # Create controller using factory
    try:
        controller = create_controller(
            controller_type=controller_type,
            config=plant_config,
            gains=gains
        )
    except Exception as e:
        logger.error(f"Failed to create controller for PSO: {e}")
        raise

    # Wrap for PSO optimization
    wrapper = PSOControllerWrapper(
        controller=controller,
        controller_type=controller_type,
        validation_enabled=default_pso_options['validation_enabled']
    )

    # Add PSO-required attributes
    wrapper.n_gains = len(gains)
    wrapper.controller_type = controller_type

    return wrapper

def get_pso_optimization_bounds(controller_type: str) -> Tuple[List[float], List[float]]:
    """Get PSO optimization bounds for controller type."""

    bounds_map = {
        'classical_smc': {
            'lower': [5.0, 5.0, 3.0, 3.0, 10.0, 1.0],
            'upper': [50.0, 40.0, 30.0, 25.0, 80.0, 15.0]
        },
        'adaptive_smc': {
            'lower': [5.0, 5.0, 3.0, 3.0, 0.5],
            'upper': [50.0, 40.0, 30.0, 25.0, 8.0]
        },
        'sta_smc': {
            'lower': [10.0, 8.0, 5.0, 5.0, 3.0, 3.0],
            'upper': [80.0, 60.0, 50.0, 40.0, 30.0, 25.0]
        },
        'hybrid_adaptive_sta_smc': {
            'lower': [5.0, 5.0, 3.0, 3.0],
            'upper': [40.0, 35.0, 25.0, 20.0]
        }
    }

    bounds = bounds_map.get(controller_type, {
        'lower': [0.1] * 6,
        'upper': [50.0] * 6
    })

    return bounds['lower'], bounds['upper']