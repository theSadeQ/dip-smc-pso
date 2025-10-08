# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 6
# Runnable: True
# Hash: 5d4c92c5

def test_control_saturation_safety():
       # Force extreme control conditions
       extreme_state = np.array([π/2, π/2, 1.0, 10.0, 10.0, 5.0])
       control = controller.compute_control(extreme_state)
       assert abs(control) <= controller.max_control