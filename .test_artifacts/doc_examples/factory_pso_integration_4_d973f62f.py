# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 4
# Runnable: False
# Hash: d973f62f

# Multi-objective cost function
def multi_objective_fitness(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = simulate(controller, duration=5.0)

    # Weighted sum of objectives
    w_itae = 1.0     # Tracking error
    w_control = 0.1  # Control effort
    w_chat = 0.05    # Chattering
    w_viol = 10.0    # Constraint violations

    cost = (w_itae * result.itae +
            w_control * result.rms_control +
            w_chat * result.chattering_index +
            w_viol * result.violation_count)

    return cost

pso = PSOTuner(
    n_particles=30,
    bounds=bounds,
    fitness_function=multi_objective_fitness
)

best_gains, best_cost = pso.optimize(max_iterations=100)