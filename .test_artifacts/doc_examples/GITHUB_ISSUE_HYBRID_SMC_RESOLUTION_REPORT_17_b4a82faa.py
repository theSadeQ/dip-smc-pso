# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 17
# Runnable: False
# Hash: b4a82faa

# example-metadata:
# runnable: false

# Property-based testing for controller interfaces
@given(st.arrays(np.float64, shape=(6,), elements=st.floats(-10, 10)))
def test_controller_always_returns_valid_output(state):
    """Property: Controllers always return valid control outputs."""
    for controller_name in ALL_CONTROLLERS:
        controller = create_controller(controller_name)
        result = controller.compute_control(state)

        assert result is not None
        assert hasattr(result, 'control')
        assert np.isfinite(result.control)