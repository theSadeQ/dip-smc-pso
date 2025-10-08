# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 19
# Runnable: True
# Hash: 6352d07e

# GOOD: Broadcasting avoids explicit loops
n_particles = 30
control_input = np.array([1.0])  # Single value
u_batch = np.broadcast_to(control_input, (n_particles,))  # Efficient view

# BAD: Explicit replication
u_batch = np.array([control_input[0] for _ in range(n_particles)])