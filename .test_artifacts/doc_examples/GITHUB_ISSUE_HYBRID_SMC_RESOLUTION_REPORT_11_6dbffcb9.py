# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 11
# Runnable: False
# Hash: 6dbffcb9

# example-metadata:
# runnable: false

class TestControllerReturnTypes:
    """Comprehensive return type validation tests."""

    @pytest.mark.parametrize("controller_name", [
        'classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc'
    ])
    def test_compute_control_never_returns_none(self, controller_name):
        """Ensure compute_control never returns None."""
        controller = create_controller(controller_name)

        test_states = [
            np.zeros(6),                           # Zero state
            np.ones(6) * 0.1,                     # Small values
            np.array([1, 0.5, -0.3, 0.1, -0.2, 0.05]),  # Mixed values
        ]

        for state in test_states:
            result = controller.compute_control(state)
            assert result is not None, f"{controller_name} returned None"
            assert hasattr(result, 'control'), f"{controller_name} missing control"