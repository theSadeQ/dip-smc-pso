# Example from: docs\reference\controllers\factory_pso_integration.md
# Index: 3
# Runnable: True
# Hash: 5dc25f06

from src.controllers.factory import create_smc_for_pso, SMCType, get_gain_bounds_for_pso
from src.optimizer.pso_optimizer import PSOTuner

# Get parameter bounds for Classical SMC
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# Define fitness function
def fitness_function(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = simulate(controller, duration=5.0)
    return result.itae + 0.1 * result.rms_control

# Initialize PSO
pso = PSOTuner(
    n_particles=30,
    bounds=bounds,
    fitness_function=fitness_function
)

# Optimize
best_gains, best_fitness = pso.optimize(max_iterations=50)
print(f"Optimal gains: {best_gains}")
print(f"Best fitness:  {best_fitness:.4f}")