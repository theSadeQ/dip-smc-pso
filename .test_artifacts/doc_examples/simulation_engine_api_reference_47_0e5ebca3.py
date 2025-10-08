# Example from: docs\api\simulation_engine_api_reference.md
# Index: 47
# Runnable: True
# Hash: 0e5ebca3

from src.simulation.orchestrators import BatchOrchestrator
from src.optimization import PSOTuner
import functools

# Create batch orchestrator
orchestrator = BatchOrchestrator(dynamics, integrator)

# Define fitness function using batch execution
def fitness_function(gains):
    # Create controller with candidate gains
    controller = create_controller('classical_smc', config, gains=gains)

    # Batch initial conditions (10 perturbations)
    batch_initial = np.random.randn(10, 6) * 0.1

    # Generate control inputs
    controls = np.zeros((10, 500))  # (batch_size, horizon)
    for i in range(10):
        for t in range(500):
            controls[i, t] = controller(t * 0.01, batch_initial[i])

    # Batch execution
    result = orchestrator.execute(
        initial_state=batch_initial,
        control_inputs=controls,
        dt=0.01,
        horizon=500
    )

    # Compute fitness (aggregate over 10 trials)
    all_states = result.get_states()  # (10, 501, 6)
    settling_times = compute_settling_times(all_states)
    return np.mean(settling_times)

# Use with PSO
tuner = PSOTuner(fitness_fn=fitness_function, bounds=[(1,50)]*6)
result = tuner.optimise()