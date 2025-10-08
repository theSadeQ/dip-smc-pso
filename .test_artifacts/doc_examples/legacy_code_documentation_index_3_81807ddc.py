# Example from: docs\implementation\legacy_code_documentation_index.md
# Index: 3
# Runnable: False
# Hash: 81807ddc

def test_sliding_surface_stability():
    """Verify that sliding surface has stable dynamics."""
    controller = ClassicalSMC(c=[1, 2, 3], eta=1.0, epsilon=0.1)

    # Test eigenvalues of sliding surface dynamics
    A_slide = controller.get_sliding_dynamics_matrix()
    eigenvals = np.linalg.eigvals(A_slide)

    # Theorem 1: All eigenvalues should be negative
    assert all(np.real(eig) < 0 for eig in eigenvals)

def test_lyapunov_decrease():
    """Verify Lyapunov function decreases along trajectories."""
    controller = AdaptiveSMC(c=[2, 3, 4], gamma=1.0)

    # Test Lyapunov function derivative
    x = np.random.rand(6)
    V_dot = controller.compute_lyapunov_derivative(x)

    # Theorem 5: Lyapunov derivative should be negative
    assert V_dot <= 0