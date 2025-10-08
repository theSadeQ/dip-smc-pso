# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 13
# Runnable: True
# Hash: d16d7cea

from src.simulation.context.simulation_context import SimulationContext

# Initialize simulation context
ctx = SimulationContext("config.yaml")

# Access components
dynamics = ctx.get_dynamics_model()
config = ctx.get_config()

# Create controller with defaults from config
controller = ctx.create_controller("classical_smc")

# Create controller with custom gains
adaptive_ctrl = ctx.create_controller("adaptive_smc", gains=[10, 5, 8, 3, 2.0])

# Run simulation
t, states, controls = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=config.simulation.duration,
    dt=config.simulation.dt,
    initial_state=config.simulation.initial_state
)