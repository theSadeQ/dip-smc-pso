# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 20
# Runnable: False
# Hash: 2abb4755

# example-metadata:
# runnable: false

# tests/utils/assertions.py

def assert_stabilized(final_state, tolerance=0.05):
    """Assert that final state is stabilized to equilibrium."""
    error = np.linalg.norm(final_state)
    assert error < tolerance, f"System not stabilized: error={error:.4f} > {tolerance}"

def assert_control_bounded(control_history, max_force):
    """Assert that all control values are within saturation limits."""
    violations = np.sum(np.abs(control_history) > max_force)
    assert violations == 0, f"Control violations: {violations} timesteps exceeded {max_force}N"

def assert_lyapunov_decreasing(lyapunov_values):
    """Assert that Lyapunov function is non-increasing."""
    diffs = np.diff(lyapunov_values)
    increasing = np.sum(diffs > 0)
    assert increasing == 0, f"Lyapunov not decreasing: {increasing} increases detected"

def assert_convergence(states, final_tolerance=0.01, settling_time=5.0, dt=0.01):
    """Assert exponential convergence to equilibrium."""
    errors = np.linalg.norm(states, axis=1)
    final_error = errors[-1]
    settling_index = int(settling_time / dt)

    assert final_error < final_tolerance, f"Final error {final_error:.4f} > {final_tolerance}"
    assert np.all(errors[settling_index:] < final_tolerance), "Not settled within settling time"