# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 6
# Runnable: False
# Hash: 84ae1d96

# example-metadata:
# runnable: false

def update_position(self, particle_idx: int) -> np.ndarray:
    """Update position for a single particle.

    Args:
        particle_idx: Index of particle to update

    Returns:
        Updated position vector
    """
    position = self.positions[particle_idx]
    velocity = self.velocities[particle_idx]

    # Position update
    position_new = position + velocity

    # Boundary handling (absorbing boundaries)
    position_new = np.clip(
        position_new,
        self.bounds_lower,
        self.bounds_upper
    )

    # Reset velocity if boundary hit
    boundary_hit = (position_new == self.bounds_lower) | (position_new == self.bounds_upper)
    if np.any(boundary_hit):
        velocity[boundary_hit] = 0.0
        self.velocities[particle_idx] = velocity

    return position_new