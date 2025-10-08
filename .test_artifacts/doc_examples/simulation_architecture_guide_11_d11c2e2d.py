# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 11
# Runnable: True
# Hash: d11c2e2d

from src.simulation.engines.simulation_runner import run_simulation
from src.controllers.factory import create_controller
from src.plant.models.dynamics import DoubleInvertedPendulum

# Create controller and dynamics
controller = create_controller('classical_smc', config=config, gains=[10, 5, 8, 3, 15, 2])
dynamics = DoubleInvertedPendulum(config.physics)

# Run simulation
t, states, controls = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=10.0,
    dt=0.01,
    initial_state=np.array([0.0, 0.1, -0.05, 0.0, 0.0, 0.0]),
    u_max=100.0,
    seed=42
)

print(f"Time points: {len(t)}")       # 1001
print(f"States shape: {states.shape}")  # (1001, 6)
print(f"Controls shape: {controls.shape}")  # (1000,)