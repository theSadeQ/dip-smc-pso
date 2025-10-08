# Example from: docs\reference\controllers\smc_algorithms_super_twisting_controller.md
# Index: 7
# Runnable: True
# Hash: d9eb7371

from src.core.simulation_runner import SimulationRunner
from src.plant.models.full import FullDynamics

# Use full dynamics for realistic chattering assessment
dynamics = FullDynamics()
runner = SimulationRunner(controller, dynamics)

result = runner.run(
    initial_state=[0.15, 0.1, 0, 0, 0, 0],
    duration=10.0,
    dt=0.001  # High frequency for chattering detection
)

# Analyze chattering index
chattering = runner.compute_chattering_index(result.control_history)
print(f"Chattering index: {chattering:.4f} (lower is better)")