# Example from: docs\test_infrastructure_documentation.md
# Index: 11
# Runnable: False
# Hash: 98f500c0

# example-metadata:
# runnable: false

@pytest.mark.property_based
@given(
    gains=lists(floats(min_value=0.1, max_value=50.0), min_size=6, max_size=6),
    initial_state=arrays(dtype=float, shape=6, elements=floats(-0.5, 0.5))
)
def test_controller_output_bounds(gains, initial_state):
    """Property test: controller output should always be bounded."""
    controller = ClassicalSMC(gains=gains)
    control_output = controller.compute_control(initial_state)

    # Property: control output must be finite and bounded
    assert np.all(np.isfinite(control_output))
    assert abs(control_output) <= controller.max_force