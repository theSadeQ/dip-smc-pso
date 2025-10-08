# Example from: docs\test_execution_guide.md
# Index: 4
# Runnable: True
# Hash: f2b4199f

def test_controller_stability(dynamics, initial_state, make_hybrid):
    """Test controller stability with standard fixtures."""
    controller = make_hybrid(gains=[0.5, 2.0, 0.8, 1.5])
    control_output = controller.compute_control(initial_state)
    assert abs(control_output) <= controller.max_force