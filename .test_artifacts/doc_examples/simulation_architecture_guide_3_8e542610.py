# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 3
# Runnable: False
# Hash: 8e542610

# example-metadata:
# runnable: false

# Simulate 30 particles with different initial conditions
n_particles = 30
x0_batch = np.random.randn(n_particles, 6) * 0.1  # (30, 6)
u_batch = np.zeros((n_particles, 100))            # (30, 100)

states_batch = simulate(x0_batch, u_batch, dt)

print(f"Batch shape: {states_batch.shape}")  # (30, 101, 6)

# Analyze each particle
for i in range(n_particles):
    final_energy = np.sum(states_batch[i, -1, :]**2)
    print(f"Particle {i}: final energy = {final_energy:.4f}")