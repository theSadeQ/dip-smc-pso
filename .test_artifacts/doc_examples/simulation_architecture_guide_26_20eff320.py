# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 26
# Runnable: False
# Hash: 20eff320

# example-metadata:
# runnable: false

# PSO fitness evaluation (30 particles)

# BAD: Sequential loop (slow)
def fitness_sequential(particles):
    costs = []
    for gains in particles:
        controller = create_controller('classical_smc', gains=gains)
        _, states, _ = run_simulation(controller, dynamics, 10.0, 0.01, x0)
        costs.append(compute_cost(states))
    return np.array(costs)

# GOOD: Vectorized batch (25x faster)
def fitness_vectorized(particles):
    x0_batch = np.tile(x0, (len(particles), 1))  # (30, 6)
    u_batch = np.zeros((len(particles), 1000))

    # Create controllers in batch
    controllers = [create_controller('classical_smc', gains=g) for g in particles]

    # Simulate all at once
    states_batch = simulate(x0_batch, u_batch, 0.01)  # (30, 1001, 6)

    # Vectorized cost computation
    costs = np.sum(states_batch[:, :, :3]**2 * dt, axis=(1, 2))
    return costs