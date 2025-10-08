# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 11
# Runnable: False
# Hash: 787043ed

# SLOW: Sequential simulation (Python loop)
def sequential_evaluation(particles, controller_factory):
    costs = []
    for gains in particles:
        controller = controller_factory(gains)
        cost = simulate(controller, T, dt)
        costs.append(cost)
    return np.array(costs)

# FAST: Vectorized simulation (NumPy operations)
def vectorized_evaluation(particles, controller_factory):
    # Single call for entire batch
    t, x_batch, u_batch, sigma_batch = simulate_system_batch(
        controller_factory=controller_factory,
        particles=particles,  # Shape: (N, D)
        sim_time=T,
        dt=dt
    )

    # Vectorized cost computation
    costs = compute_costs_batch(t, x_batch, u_batch, sigma_batch)
    return costs  # Shape: (N,)

# Speedup: ~20-30x for N=30 particles