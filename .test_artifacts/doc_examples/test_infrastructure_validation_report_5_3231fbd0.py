# Example from: docs\test_infrastructure_validation_report.md
# Index: 5
# Runnable: True
# Hash: 3231fbd0

@pytest.mark.property_based
@given(
    gains=lists(floats(min_value=0.1, max_value=50.0), min_size=6, max_size=6),
    initial_state=arrays(dtype=float, shape=6, elements=floats(-0.5, 0.5))
)
def test_controller_boundedness_property(gains, initial_state):
    """Universal property: controller output must always be bounded."""
    # Mathematical guarantee: |u(t)| ≤ u_max ∀ t ≥ 0