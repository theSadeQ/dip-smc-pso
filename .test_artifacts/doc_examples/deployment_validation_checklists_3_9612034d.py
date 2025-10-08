# Example from: docs\deployment_validation_checklists.md
# Index: 3
# Runnable: False
# Hash: 9612034d

def test_controller_factory_integration():
    """Test controller factory integration."""
    factory = ControllerFactory()

    # Test all controller types
    controller_types = ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

    for controller_type in controller_types:
        # Test instantiation
        controller = factory.create_controller(controller_type, test_config)
        assert controller is not None

        # Test basic functionality
        control_signal = controller.compute_control(test_state, test_target)
        assert isinstance(control_signal, (int, float))
        assert not np.isnan(control_signal)

        # Test parameter validation
        assert controller.validate_parameters()

    return True