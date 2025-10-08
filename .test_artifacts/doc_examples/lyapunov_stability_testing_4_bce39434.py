# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 4
# Runnable: False
# Hash: bce39434

def test_region_of_attraction():
    """Verify estimated region of attraction"""
    # Sample initial states from estimated ROA
    R = 0.5  # Estimated ROA radius
    test_states = sample_sphere(center=[0,0,0,0], radius=R, n_samples=100)

    for initial_state in test_states:
        trajectory = simulate(controller, dynamics, initial_state, duration=10.0)
        final_state = trajectory[-1]

        # Must converge to equilibrium
        assert np.linalg.norm(final_state) < 0.05, \
            f"Failed to converge from {initial_state}"