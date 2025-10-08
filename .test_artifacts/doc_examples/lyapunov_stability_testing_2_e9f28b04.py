# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 2
# Runnable: False
# Hash: e9f28b04

# example-metadata:
# runnable: false

@given(state=valid_states())
def test_lyapunov_decrease(state):
    """dV/dt ≤ 0 along trajectories"""
    # Compute V at current state
    V_t = lyapunov_function(state)

    # Simulate one time step
    u = controller.compute_control(state)
    state_next = dynamics.step(state, u, dt=0.01)

    V_next = lyapunov_function(state_next)

    # Allow small numerical tolerance
    assert V_next <= V_t + 1e-6, \
        f"V increased: {V_t} → {V_next} (Δ={V_next - V_t})"