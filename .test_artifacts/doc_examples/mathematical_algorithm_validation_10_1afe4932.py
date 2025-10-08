# Example from: docs\mathematical_algorithm_validation.md
# Index: 10
# Runnable: False
# Hash: 1afe4932

# example-metadata:
# runnable: false

def test_end_to_end_mathematical_properties():
    """Test mathematical properties in complete system."""

    # Initialize system
    system = DoubleInvertedPendulum()
    controller = ClassicalSMC()

    # Initial condition away from equilibrium
    x0 = np.array([0.2, 0.1, 0.0, 0.0, 0.0, 0.0])
    target = np.zeros(6)

    # Simulate system
    trajectory = simulate_system(system, controller, x0, target, t_final=10.0)

    # Mathematical property verification

    # 1. Verify Lyapunov function decreases
    V_values = [controller.compute_lyapunov_function(state) for state in trajectory.states]
    assert np.all(np.diff(V_values) <= 0), "Lyapunov function must be non-increasing"

    # 2. Verify convergence to target
    final_error = np.linalg.norm(trajectory.states[-1] - target)
    assert final_error < 0.01, f"Final error {final_error} too large"

    # 3. Verify control signal bounds
    max_control = np.max(np.abs(trajectory.controls))
    assert max_control <= controller.u_max, "Control signal exceeds limits"