# Example from: docs\analysis\HYBRID_SMC_FIX_TECHNICAL_DOCUMENTATION.md
# Index: 13
# Runnable: False
# Hash: 6dd2d335

def test_controller_return_types():
    """Comprehensive return type validation tests."""
    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']

    for controller_name in controllers:
        controller = create_controller(controller_name)
        result = controller.compute_control(test_state)

        # Critical validations
        assert result is not None, f"{controller_name} returned None"
        assert hasattr(result, 'control'), f"{controller_name} missing control"
        assert isinstance(result.control, (int, float)), f"Invalid control type"
        assert np.isfinite(result.control), f"Non-finite control value"