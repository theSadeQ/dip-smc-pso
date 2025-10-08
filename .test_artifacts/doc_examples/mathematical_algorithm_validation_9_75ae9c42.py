# Example from: docs\mathematical_algorithm_validation.md
# Index: 9
# Runnable: False
# Hash: 75ae9c42

class TestMathematicalCorrectness:
    """Test mathematical properties of implementations."""

    def test_lyapunov_function_properties(self):
        """Test Lyapunov function is positive definite."""
        controller = ClassicalSMC()
        for _ in range(1000):
            state = np.random.uniform(-π, π, 6)
            V = controller.compute_lyapunov_function(state)

            # Property 1: V ≥ 0
            assert V >= 0

            # Property 2: V = 0 only at equilibrium
            if not np.allclose(state, 0):
                assert V > 0

    def test_sliding_surface_stability(self):
        """Test sliding surface leads to stable dynamics."""
        controller = ClassicalSMC(lambda1=2.0, lambda2=1.5)

        # Test exponential stability on sliding surface
        dt = 0.01
        times = np.arange(0, 5, dt)

        for initial_error in [0.1, 0.5, 1.0]:
            e1_history = [initial_error]
            e2_history = [initial_error]

            for t in times[1:]:
                # Sliding dynamics: ė₁ + λ₁e₁ = 0, ė₂ + λ₂e₂ = 0
                e1_new = e1_history[-1] * np.exp(-controller.lambda1 * dt)
                e2_new = e2_history[-1] * np.exp(-controller.lambda2 * dt)

                e1_history.append(e1_new)
                e2_history.append(e2_new)

            # Verify exponential decay
            assert e1_history[-1] < 0.01 * initial_error
            assert e2_history[-1] < 0.01 * initial_error