# Example from: docs\mathematical_foundations\boundary_layer_derivations.md
# Index: 3
# Runnable: True
# Hash: 730cda44

def test_lyapunov_decrease():
    # Verify that V̇ < 0 outside the ultimate bound
    sigma = np.linspace(-1, 1, 100)
    for s in sigma:
        if abs(s) > ultimate_bound:
            V_dot = compute_lyapunov_derivative(s)
            assert V_dot < 0