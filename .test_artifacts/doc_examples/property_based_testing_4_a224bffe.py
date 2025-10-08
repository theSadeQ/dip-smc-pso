# Example from: docs\testing\guides\property_based_testing.md
# Index: 4
# Runnable: False
# Hash: a224bffe

# example-metadata:
# runnable: false

@given(state=valid_states())
def test_lyapunov_decrease(state):
    """Lyapunov function decreases along trajectories"""
    # Compute V(x) at current state
    V_current = lyapunov_function(state)

    # Simulate one timestep
    u = controller.compute_control(state)
    next_state = dynamics.step(state, u, dt=0.01)
    V_next = lyapunov_function(next_state)

    # V must decrease (or stay same if at equilibrium)
    assert V_next <= V_current + 1e-6, \
        f"Lyapunov increased: {V_current} -> {V_next}"