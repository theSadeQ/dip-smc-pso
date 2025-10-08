# Example from: docs\pso_factory_integration_patterns.md
# Index: 8
# Runnable: True
# Hash: cae87d7c

def high_performance_pso_integration():
    """High-performance PSO integration with optimizations."""

    # Pre-compile Numba functions for controller evaluation
    from numba import jit

    @jit(nopython=True)
    def fast_control_computation(state, gains, max_force):
        """Numba-compiled control computation."""
        # Simplified controller logic for speed
        k1, k2, lam1, lam2, K, kd = gains

        # Sliding surface
        s = lam1 * state[0] + lam2 * state[1] + state[3] + state[4]

        # Control law
        u = -K * np.tanh(s / 0.01)

        # Saturation
        return np.clip(u, -max_force, max_force)

    # Vectorized fitness evaluation
    @jit(nopython=True)
    def vectorized_fitness_evaluation(gains_matrix, states_batch):
        """Vectorized evaluation for multiple gain sets."""
        n_particles, n_gains = gains_matrix.shape
        n_states, state_dim = states_batch.shape

        fitness_values = np.zeros(n_particles)

        for i in range(n_particles):
            gains = gains_matrix[i]
            total_cost = 0.0

            for j in range(n_states):
                state = states_batch[j]
                control = fast_control_computation(state, gains, 150.0)
                total_cost += np.sum(state**2) + 0.1 * control**2

            fitness_values[i] = total_cost / n_states

        return fitness_values

    # High-performance PSO workflow
    def optimized_pso_workflow():
        """Optimized PSO workflow using vectorized operations."""

        # Pre-generate test states for evaluation
        test_states = generate_test_state_batch(1000)

        # Vectorized fitness function
        def fitness_function(gains_matrix: np.ndarray) -> np.ndarray:
            """Vectorized fitness evaluation."""
            if gains_matrix.ndim == 1:
                gains_matrix = gains_matrix.reshape(1, -1)

            return vectorized_fitness_evaluation(gains_matrix, test_states)

        # Use vectorized PSO
        from src.optimization.algorithms.vectorized_pso import VectorizedPSO

        optimizer = VectorizedPSO(
            fitness_function=fitness_function,
            n_particles=50,
            n_dimensions=6,
            bounds=get_gain_bounds_for_pso(SMCType.CLASSICAL),
            max_iterations=100
        )

        return optimizer.optimize()