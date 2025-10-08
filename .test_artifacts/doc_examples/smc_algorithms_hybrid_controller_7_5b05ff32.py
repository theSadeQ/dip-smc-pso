# Example from: docs\reference\controllers\smc_algorithms_hybrid_controller.md
# Index: 7
# Runnable: True
# Hash: 5b05ff32

from src.core.simulation_runner import SimulationRunner
from src.plant.models.simplified import SimplifiedDynamics

dynamics = SimplifiedDynamics()
runner = SimulationRunner(controller, dynamics)

result = runner.run(
    initial_state=[0.2, 0.15, 0, 0, 0, 0],  # Large disturbance
    duration=15.0,
    dt=0.01
)

# Analyze mode switching history
mode_history = result.controller_history['active_mode']
switches = np.diff(mode_history).nonzero()[0]
print(f"Mode switches: {len(switches)} times")