# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 7
# Runnable: False
# Hash: 5d925829

# example-metadata:
# runnable: false

def test_all_controllers_operational():
    """Verify all 4 controllers remain operational after hybrid fix."""
    controllers = ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']

    for controller_name in controllers:
        controller = create_controller(controller_name)
        result = controller.compute_control(test_state)

        assert result is not None, f"{controller_name} returned None"
        assert hasattr(result, 'control'), f"{controller_name} missing control"
        assert np.isfinite(result.control), f"{controller_name} non-finite control"

    print("✅ All 4 controllers operational")