# Example from: docs\test_infrastructure_documentation.md
# Index: 1
# Runnable: True
# Hash: b5cb2707

@pytest.mark.unit
def test_sliding_surface_computation():
    """Test sliding surface value computation for classical SMC."""
    controller = ClassicalSMC(gains=[10, 5, 8, 3, 15, 2])
    state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
    surface_value = controller.compute_sliding_surface(state, np.zeros(6))
    assert isinstance(surface_value, float)