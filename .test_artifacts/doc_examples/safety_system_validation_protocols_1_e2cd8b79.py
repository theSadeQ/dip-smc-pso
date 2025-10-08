# Example from: docs\safety_system_validation_protocols.md
# Index: 1
# Runnable: False
# Hash: e2cd8b79

# example-metadata:
# runnable: false

# MANDATORY: 100% line coverage
def test_saturation_boundary_conditions():
    """Test control signal saturation at exact limits."""
    assert saturate_control_signal(10.1, 10.0) == 10.0
    assert saturate_control_signal(-10.1, -10.0) == -10.0

@hypothesis.given(control_signal=st.floats(min_value=-1000, max_value=1000))
def test_saturation_property_based(control_signal):
    """Property-based test for saturation function."""
    result = saturate_control_signal(control_signal, 10.0)
    assert -10.0 <= result <= 10.0