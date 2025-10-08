# Example from: docs\architecture\controller_system_architecture.md
# Index: 14
# Runnable: True
# Hash: 2baf61a6

from numba import jit, prange
import numpy as np

class PerformanceOptimizedController:
    """Performance-optimized controller with Numba acceleration."""

    @staticmethod
    @jit(nopython=True, cache=True)
    def compute_sliding_surface_numba(
        state: np.ndarray,
        gains: np.ndarray
    ) -> float:
        """Numba-accelerated sliding surface computation."""

        # Extract state components
        theta1, theta2, x, theta1_dot, theta2_dot, x_dot = state
        lambda1, lambda2, c1, c2, kc, lambda_c = gains

        # Compute sliding surface
        s = (lambda1 * theta1_dot + c1 * theta1 +
             lambda2 * theta2_dot + c2 * theta2 +
             kc * (x_dot + lambda_c * x))

        return s

    @staticmethod
    @jit(nopython=True, cache=True)
    def batch_control_computation(
        states: np.ndarray,
        gains: np.ndarray,
        controller_params: np.ndarray
    ) -> np.ndarray:
        """Vectorized control computation for batch processing."""

        n_samples = states.shape[0]
        controls = np.zeros(n_samples)

        for i in prange(n_samples):
            controls[i] = compute_control_single(states[i], gains, controller_params)

        return controls