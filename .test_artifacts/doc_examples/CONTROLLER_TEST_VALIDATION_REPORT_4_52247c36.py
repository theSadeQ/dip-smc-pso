# Example from: docs\reports\CONTROLLER_TEST_VALIDATION_REPORT.md
# Index: 4
# Runnable: True
# Hash: 52247c36

# Fixed dynamics computation interface
result = dynamics.compute_dynamics(test_state, np.array([1.0]))
assert result.success, "Dynamics computation should succeed"
state_dot = result.state_derivative  # Fixed: was using result directly