# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 9
# Runnable: False
# Hash: d8c16864

def test_controller_interface_compliance():
    """Comprehensive interface compliance testing."""
    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']

    for controller_name in controllers:
        controller = create_controller(controller_name, test_config)

        # Test 1: Valid return type
        result = controller.compute_control(test_state)
        assert result is not None, f"{controller_name} returned None"
        assert hasattr(result, 'control'), f"{controller_name} missing control attribute"

        # Test 2: Type consistency
        assert isinstance(result.control, (int, float)), f"{controller_name} invalid control type"

        # Test 3: Finite values
        assert np.isfinite(result.control), f"{controller_name} non-finite control"