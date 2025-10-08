# Example from: docs\api\simulation_engine_api_reference.md
# Index: 23
# Runnable: True
# Hash: 6d8ae705

from src.simulation import SimulationRunner
from src.plant.models import LowRankDIPDynamics

# Create runner
dynamics = LowRankDIPDynamics(config.plant)
runner = SimulationRunner(dynamics, dt=0.01, max_time=10.0)

# Run simulation
result = runner.run_simulation(
    initial_state=np.array([0, 0.1, 0.1, 0, 0, 0]),
    controller=controller,
    sim_time=5.0
)

# Check result
if result['success']:
    print(f"Simulation completed: {result['step_count']} steps")
    print(f"Final state: {result['final_state']}")
else:
    print(f"Simulation failed: {result['error']}")

# Access history
for i, run in enumerate(runner.simulation_history):
    print(f"Run {i}: {run['time'].shape[0]} steps")