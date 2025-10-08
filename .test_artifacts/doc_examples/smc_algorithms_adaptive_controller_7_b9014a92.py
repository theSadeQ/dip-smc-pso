# Example from: docs\reference\controllers\smc_algorithms_adaptive_controller.md
# Index: 7
# Runnable: True
# Hash: b9014a92

from src.core.simulation_runner import SimulationRunner
from src.plant.models.simplified import SimplifiedDynamics

# Create simulation with adaptive controller
dynamics = SimplifiedDynamics()
runner = SimulationRunner(controller, dynamics)

# Run with uncertainty
result = runner.run(
    initial_state=[0.1, 0.05, 0, 0, 0, 0],
    duration=10.0,
    dt=0.01
)

# Analyze gain adaptation
adaptive_gains = result.history['adaptive_gain']
print(f"Final adapted gain: {adaptive_gains[-1]:.2f}")