# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 5
# Runnable: False
# Hash: 745e9041

# example-metadata:
# runnable: false

def test_lyapunov_decrease_property():
    """Test Lyapunov decrease property: V̇ < 0 when |σ| > 0."""
    controller = create_test_controller()

    # Test states with non-zero sliding surface values
    test_states = [
        np.array([0.0, 0.1, 0.0, 0.0, 0.0, 0.0]),   # Pendulum 1 displaced
        np.array([0.0, 0.0, 0.1, 0.0, 0.0, 0.0]),   # Pendulum 2 displaced
        np.array([0.0, 0.05, 0.05, 0.0, 0.1, 0.1]), # Both displaced with velocity
    ]

    history = {}

    for state in test_states:
        result = controller.compute_control(state, (), history)

        # Extract sliding surface from history
        assert 'sigma' in history
        sigma = history['sigma'][-1]

        # Lyapunov function V = 0.5 * sigma^2
        V = 0.5 * sigma**2

        # For non-zero sigma, ensure control acts to reduce V
        if abs(sigma) > 1e-6:
            # Control should oppose sigma to drive V̇ < 0
            # For classical SMC: u = u_eq - K*sat(σ/ε) - kd*σ
            # The robust term -K*sat(σ/ε) should have opposite sign to σ
            u_robust = history['u_robust'][-1]

            # Robust control should oppose sliding surface
            assert np.sign(u_robust) == -np.sign(sigma) or abs(sigma) < controller.epsilon0