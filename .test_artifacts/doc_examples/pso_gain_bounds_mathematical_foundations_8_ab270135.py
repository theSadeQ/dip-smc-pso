# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 8
# Runnable: False
# Hash: ab270135

# example-metadata:
# runnable: false

class VectorizedBoundsValidator:
    """
    Optimized bounds validation for PSO swarm evaluation.
    """

    def __init__(self, controller_type: str):
        self.controller_type = controller_type
        self.bounds = self._get_optimized_bounds()

    def validate_swarm(self, particles: np.ndarray) -> np.ndarray:
        """
        Vectorized validation for entire PSO swarm.

        Parameters:
        particles: shape (n_particles, n_dims)

        Returns:
        valid_mask: shape (n_particles,) boolean array
        """
        n_particles = particles.shape[0]
        valid_mask = np.ones(n_particles, dtype=bool)

        # Vectorized bounds checking
        for i, (min_val, max_val) in enumerate(self.bounds):
            valid_mask &= (particles[:, i] >= min_val) & (particles[:, i] <= max_val)

        # Controller-specific constraints
        if self.controller_type == "sta_smc":
            # K1 > K2 constraint
            valid_mask &= particles[:, 0] > particles[:, 1]

            # Issue #2 damping constraints
            lambda1, lambda2 = particles[:, 4], particles[:, 5]
            k1, k2 = particles[:, 2], particles[:, 3]

            zeta1 = lambda1 / (2 * np.sqrt(k1))
            zeta2 = lambda2 / (2 * np.sqrt(k2))

            damping_ok = (zeta1 >= 0.69) & (zeta1 <= 0.8) & (zeta2 >= 0.69) & (zeta2 <= 0.8)
            valid_mask &= damping_ok

        return valid_mask