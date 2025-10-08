# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 7
# Runnable: False
# Hash: fa540dc3

# example-metadata:
# runnable: false

def test_lyapunov_averaged_decrease(state):
    """Check V decreases on average over window"""
    window_size = 10  # Average over 10 steps

    V_values = []
    for _ in range(window_size):
        V = lyapunov_function(state)
        V_values.append(V)

        u = controller.compute_control(state)
        state = dynamics.step(state, u, dt=0.01)

    # Moving average should decrease
    avg_first_half = np.mean(V_values[:5])
    avg_second_half = np.mean(V_values[5:])

    assert avg_second_half < avg_first_half