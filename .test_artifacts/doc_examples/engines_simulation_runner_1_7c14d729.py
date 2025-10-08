# Example from: docs\reference\simulation\engines_simulation_runner.md
# Index: 1
# Runnable: True
# Hash: 7c14d729

from src.simulation.engines.simulation_runner import run_simulation, SimulationRunner
from src.controllers.smc.algorithms.classical import ClassicalSMC
from src.plant.models.simplified import SimplifiedDynamics

# Create controller and dynamics
config = ClassicalSMCConfig(
    surface_gains=[10.0, 8.0, 15.0, 12.0],
    switching_gain=50.0,
    max_force=100.0
)
controller = ClassicalSMC(config)
dynamics = SimplifiedDynamics()

# Run simulation (functional API)
result = run_simulation(
    controller=controller,
    dynamics=dynamics,
    initial_state=[0.1, 0.05, 0, 0, 0, 0],  # [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
    duration=10.0,
    dt=0.01
)

print(f"Final tracking error: {np.linalg.norm(result.states[-1, :2]):.4f}")