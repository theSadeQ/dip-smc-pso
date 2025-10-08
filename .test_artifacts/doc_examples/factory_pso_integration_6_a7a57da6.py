# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 6
# Runnable: True
# Hash: a7a57da6

# Fitness with constraint penalties
def constrained_fitness(gains):
    # Create controller
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)

    # Validate gains first (cheap check)
    from src.controllers.smc.core.gain_validation import validate_all_criteria

    validation_config = {
        'u_max': 100.0,
        'omega_s': 2*np.pi*100,
        'Delta_max': 20.0,
        'u_eq_max': 80.0,
    }

    results = validate_all_criteria(gains, validation_config)

    # Heavy penalty for invalid gains
    if not all(results.values()):
        return 1e6  # Return worst fitness

    # Simulate only if gains valid
    result = simulate(controller, duration=5.0)
    return result.itae

pso = PSOTuner(n_particles=30, bounds=bounds, fitness_function=constrained_fitness)
best_gains, _ = pso.optimize(max_iterations=100)