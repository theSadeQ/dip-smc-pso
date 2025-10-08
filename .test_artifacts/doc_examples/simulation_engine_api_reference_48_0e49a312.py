# Example from: docs\api\simulation_engine_api_reference.md
# Index: 48
# Runnable: True
# Hash: 0e49a312

from src.simulation.orchestrators import ParallelOrchestrator

# Create parallel orchestrator (4 worker threads)
orchestrator = ParallelOrchestrator(
    dynamics=dynamics,
    integrator=integrator,
    num_workers=4
)

# Execute parameter sweep
param_grid = generate_parameter_combinations()  # (1000, n_params)
results = orchestrator.execute_parameter_sweep(param_grid)