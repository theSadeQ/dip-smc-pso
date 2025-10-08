# Example from: docs\mathematical_algorithm_validation.md
# Index: 8
# Runnable: True
# Hash: 0664d84e

# Mathematical definition: vᵢ^(t+1) = χ[w·vᵢ^t + c₁r₁(pᵢ - xᵢ^t) + c₂r₂(g - xᵢ^t)]
def update_velocity(self, particle_idx):
    r1, r2 = np.random.random(2)
    velocity = self.chi * (
        self.w * self.velocities[particle_idx] +
        self.c1 * r1 * (self.personal_best[particle_idx] - self.positions[particle_idx]) +
        self.c2 * r2 * (self.global_best - self.positions[particle_idx])
    )
    return velocity