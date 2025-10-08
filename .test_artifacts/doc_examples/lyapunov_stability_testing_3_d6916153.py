# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 3
# Runnable: False
# Hash: d6916153

# example-metadata:
# runnable: false

def test_finite_time_reaching():
    """Sliding surface reached in finite time"""
    initial_state = np.array([0.5, -0.3, 1.0, -0.8])
    sigma_0 = sliding_surface(initial_state)

    trajectory = simulate(controller, dynamics, initial_state, duration=5.0)

    # Find first time σ crosses zero
    t_reach = None
    for i, state in enumerate(trajectory):
        sigma = sliding_surface(state)
        if abs(sigma) < 0.01:  # Threshold for "reached"
            t_reach = i * 0.01
            break

    assert t_reach is not None, "Did not reach sliding surface"

    # Verify theoretical bound: t_reach ≤ |σ(0)| / η
    eta = 0.1  # Known reaching constant
    t_theoretical = abs(sigma_0) / eta

    assert t_reach <= t_theoretical * 1.2, \  # Allow 20% tolerance
        f"Took too long: {t_reach}s > {t_theoretical}s"