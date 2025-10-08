# Example from: docs\optimization_simulation\guide.md
# Index: 3
# Runnable: True
# Hash: e97d8c5b

from src.simulation.engines.simulation_runner import run_simulation
from src.controllers import ClassicalSMC
from src.plant.models.simplified import SimplifiedDIPDynamics, SimplifiedDIPConfig

# Setup dynamics
config = SimplifiedDIPConfig.create_default()
dynamics = SimplifiedDIPDynamics(config)

# Setup controller
controller = ClassicalSMC(
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    boundary_layer=0.01
)

# Initial state
x0 = [0.0, 0.1, -0.05, 0.0, 0.0, 0.0]  # Small perturbation from upright

# Run simulation
t_arr, x_arr, u_arr = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=x0
)

# Analyze results
print(f"Simulated {len(t_arr)} time steps")
print(f"Final state: {x_arr[-1]}")
print(f"Max control: {np.max(np.abs(u_arr)):.2f} N")