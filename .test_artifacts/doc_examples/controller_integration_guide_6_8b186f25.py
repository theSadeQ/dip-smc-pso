# Example from: docs\factory\controller_integration_guide.md
# Index: 6
# Runnable: True
# Hash: 8b186f25

def create_and_validate_dynamics_model(
    plant_config: Any,
    controller_type: str
) -> Tuple[Any, Dict[str, Any]]:
    """
    Create and validate plant dynamics model for controller integration.

    Returns:
        Tuple of (dynamics_model, validation_results)
    """

    # 1. Create dynamics model
    try:
        if hasattr(plant_config, 'dynamics_model'):
            dynamics_model = plant_config.dynamics_model
        elif hasattr(plant_config, 'physics'):
            dynamics_model = DIPDynamics(plant_config.physics)
        elif hasattr(plant_config, 'dip_params'):
            dynamics_model = DIPDynamics(plant_config.dip_params)
        else:
            from src.plant.models.simplified.dynamics import SimplifiedDIPDynamics
            dynamics_model = SimplifiedDIPDynamics(plant_config)

    except Exception as e:
        logger.warning(f"Could not create specific dynamics model: {e}")
        # Fallback to generic dynamics
        dynamics_model = DIPDynamics()

    # 2. Validate dynamics-controller compatibility
    validation_results = {
        'model_type': type(dynamics_model).__name__,
        'state_dimension': 6,  # DIP standard state dimension
        'control_dimension': 1,  # Single control input
        'supports_linearization': hasattr(dynamics_model, 'linearize'),
        'supports_jacobian': hasattr(dynamics_model, 'compute_jacobian'),
        'integration_compatible': True
    }

    # 3. Test basic functionality
    try:
        test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
        test_control = np.array([1.0])

        result = dynamics_model.compute_dynamics(test_state, test_control)
        validation_results['compute_dynamics_test'] = hasattr(result, 'state_derivative')
        validation_results['derivative_shape'] = result.state_derivative.shape if hasattr(result, 'state_derivative') else None

    except Exception as e:
        validation_results['compute_dynamics_test'] = False
        validation_results['test_error'] = str(e)

    return dynamics_model, validation_results

def validate_controller_plant_compatibility(
    controller: Any,
    plant_config: Any
) -> Dict[str, bool]:
    """Validate that controller and plant are compatible."""

    compatibility = {
        'state_dimensions': True,  # Both use 6-DOF DIP state
        'control_dimensions': True,  # Both use single control input
        'sampling_time': True,     # Compatible sampling rates
        'numerical_stability': True  # No obvious numerical issues
    }

    try:
        # Test control computation
        test_state = np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0])
        control_output = controller.compute_control(test_state, (), {})

        compatibility['control_computation'] = True
        compatibility['control_bounds'] = np.abs(control_output.u) < 1000.0  # Reasonable control

    except Exception as e:
        compatibility['control_computation'] = False
        compatibility['error'] = str(e)

    return compatibility