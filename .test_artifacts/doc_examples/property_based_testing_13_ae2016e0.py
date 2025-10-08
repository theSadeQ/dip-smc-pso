# Example from: docs\testing\guides\property_based_testing.md
# Index: 13
# Runnable: False
# Hash: ae2016e0

# example-metadata:
# runnable: false

@given(state=valid_states())
def test_sliding_surface_attractivity(state):
    """Sliding surface must be attractive from any state"""
    sigma_values = []

    for t in range(100):  # 1 second simulation
        sigma = sliding_surface(state)
        sigma_values.append(abs(sigma))

        u = controller.compute_control(state)
        state = dynamics.step(state, u, dt=0.01)

    # Σ must decrease on average
    initial_sigma = sigma_values[0]
    final_sigma = sigma_values[-1]

    assert final_sigma < initial_sigma or initial_sigma < 0.01, \
        f"Sliding surface not attractive: {initial_sigma} -> {final_sigma}"