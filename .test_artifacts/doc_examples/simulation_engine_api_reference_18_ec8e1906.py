# Example from: docs\api\simulation_engine_api_reference.md
# Index: 18
# Runnable: True
# Hash: ec8e1906

from src.simulation import run_simulation
from src.controllers import create_controller
from src.plant.models import LowRankDIPDynamics
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller(
    'classical_smc',
    config=config,
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0]
)

# Create dynamics model
dynamics = LowRankDIPDynamics(config.plant)

# Run simulation
t, x, u = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=[0, 0.1, 0.1, 0, 0, 0],  # Small perturbation
    u_max=100.0,  # Saturation limit
    seed=42  # Reproducibility
)

# Analyze results
print(f"Simulation steps: {len(t)-1}")
print(f"Final state: {x[-1]}")
print(f"Max control: {np.max(np.abs(u)):.2f} N")