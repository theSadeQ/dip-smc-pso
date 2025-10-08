# Example from: docs\reference\controllers\smc_algorithms_classical_controller.md
# Index: 7
# Runnable: True
# Hash: 91652f9a

from src.core.simulation_runner import SimulationRunner
from src.plant.models.simplified import SimplifiedDynamics

# Create simulation components
dynamics = SimplifiedDynamics()
runner = SimulationRunner(controller, dynamics)

# Run simulation
result = runner.run(
    initial_state=[0.1, 0.05, 0, 0, 0, 0],  # [θ1, θ2, θ̇1, θ̇2, x, ẋ]
    duration=5.0,
    dt=0.01
)

# Analyze results
print(f"Settling time: {result.metrics.settling_time:.2f}s")
print(f"Overshoot: {result.metrics.overshoot:.1f}%")