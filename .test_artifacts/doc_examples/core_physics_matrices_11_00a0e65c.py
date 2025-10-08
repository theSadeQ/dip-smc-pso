# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 11
# Runnable: False
# Hash: 00a0e65c

# example-metadata:
# runnable: false

def compute_kinetic_energy(state, physics):
    """Compute kinetic energy using M(q)."""
    M = physics.compute_inertia_matrix(state)
    q_dot = state[3:]  # Velocities
    T = 0.5 * q_dot.T @ M @ q_dot
    return T

def compute_potential_energy(state, config):
    """Compute potential energy."""
    _, theta1, theta2, _, _, _ = state
    m1, m2 = config.pendulum1_mass, config.pendulum2_mass
    L1, Lc1, Lc2 = config.pendulum1_length, config.pendulum1_com, config.pendulum2_com
    g = config.gravity

    V = m1 * g * Lc1 * np.cos(theta1) + m2 * g * (L1 * np.cos(theta1) + Lc2 * np.cos(theta2))
    return V

# Total mechanical energy
T = compute_kinetic_energy(state, physics)
V = compute_potential_energy(state, config)
E_total = T + V
print(f"Total energy: {E_total:.4f} J")