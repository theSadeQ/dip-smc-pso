# Example from: docs\testing\theory\lyapunov_stability_testing.md
# Index: 6
# Runnable: True
# Hash: f3fd28ac

TOLERANCE = 1e-6

def test_lyapunov_with_tolerance(state):
    V_next = lyapunov_function(next_state)
    V_current = lyapunov_function(state)

    # Use relative tolerance for small V values
    if V_current < 1e-3:
        assert V_next <= V_current + TOLERANCE
    else:
        assert V_next <= V_current * (1 + TOLERANCE)