# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 5
# Runnable: False
# Hash: e12742e5

def update_velocity(self, particle_idx: int) -> np.ndarray:
    """Update velocity for a single particle.

    Args:
        particle_idx: Index of particle to update

    Returns:
        Updated velocity vector
    """
    # Current state
    position = self.positions[particle_idx]
    velocity = self.velocities[particle_idx]
    p_best = self.personal_best_positions[particle_idx]
    g_best = self.global_best_position

    # Random factors
    r1 = np.random.random(self.n_dimensions)
    r2 = np.random.random(self.n_dimensions)

    # Inertia term
    inertia_term = self.inertia_weight * velocity

    # Cognitive term (personal best attraction)
    cognitive_term = self.cognitive_weight * r1 * (p_best - position)

    # Social term (global best attraction)
    social_term = self.social_weight * r2 * (g_best - position)

    # Combined velocity update
    velocity_new = inertia_term + cognitive_term + social_term

    # Velocity clamping (if enabled)
    if self.velocity_clamping:
        v_max = 0.2 * (self.bounds_upper - self.bounds_lower)
        velocity_new = np.clip(velocity_new, -v_max, v_max)

    return velocity_new