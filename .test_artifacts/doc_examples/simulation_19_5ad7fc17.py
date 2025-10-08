# Example from: docs\guides\api\simulation.md
# Index: 19
# Runnable: True
# Hash: 5ad7fc17

# Batch evaluation for PSO fitness function
def batch_fitness_function(gains_array):
    """Evaluate controller on multiple scenarios."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains_array)

    # Test scenarios
    scenarios = [
        np.array([0, 0, 0.1, 0, 0.15, 0]),   # Nominal
        np.array([0, 0, 0.2, 0, 0.25, 0]),   # Large angles
        np.array([0.1, 0, 0.15, 0, 0.2, 0]), # Cart offset
    ]
    initial_conditions = np.array(scenarios)

    # Run batch
    results = run_batch_simulation(controller, dynamics, initial_conditions, sim_params)

    # Compute average performance
    ise = np.mean(np.sum(results[:, :, 2:4]**2, axis=(1, 2)))
    return ise

# Use with PSO
from src.optimizer import PSOTuner

tuner = PSOTuner(
    controller_type=SMCType.CLASSICAL,
    bounds=get_gain_bounds_for_pso(SMCType.CLASSICAL),
    cost_function=batch_fitness_function
)
best_gains, best_cost = tuner.optimize()