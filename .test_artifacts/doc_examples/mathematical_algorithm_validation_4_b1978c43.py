# Example from: docs\mathematical_algorithm_validation.md
# Index: 4
# Runnable: False
# Hash: b1978c43

def update_particles(self):
    """Update particle velocities and positions."""
    for i in range(self.n_particles):
        # Random coefficients
        r1, r2 = np.random.random(2)

        # Velocity update with constriction factor
        self.velocities[i] = self.chi * (
            self.w * self.velocities[i] +
            self.c1 * r1 * (self.personal_best_positions[i] - self.positions[i]) +
            self.c2 * r2 * (self.global_best_position - self.positions[i])
        )

        # Position update
        self.positions[i] += self.velocities[i]

        # Boundary handling
        self.positions[i] = np.clip(self.positions[i], self.bounds_min, self.bounds_max)