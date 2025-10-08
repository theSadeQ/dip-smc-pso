# Example from: docs\reference\optimization\algorithms_pso_optimizer.md
# Index: 8
# Runnable: False
# Hash: 16912fae

# Optimize for robustness across parameter uncertainty
def robust_cost(gains):
    controller_factory = lambda: create_smc_for_pso(SMCType.ADAPTIVE, gains)

    # Test across multiple scenarios
    costs = []
    for mass_variation in [0.8, 1.0, 1.2]:  # ±20% mass uncertainty
        dynamics = SimplifiedDynamics(cart_mass=mass_variation * 1.0)
        result = simulate(controller_factory(), dynamics, duration=10.0)
        costs.append(compute_ISE(result.states))

    # Return worst-case cost (robust optimization)
    return max(costs)

pso = PSOTuner(
    controller_factory=lambda g: None,  # Not used, cost computes internally
    bounds=([0.1]*5, [100.0]*5),  # Adaptive SMC: 5 gains
    fitness_function=robust_cost,
    n_particles=50,
    max_iter=150
)

robust_gains, worst_case_cost = pso.optimize()