# Example from: docs\controllers\mpc_technical_guide.md
# Index: 27
# Runnable: True
# Hash: eb4eab3a

from src.core.simulation_runner import SimulationRunner

# Create MPC controller
mpc = MPCController(dynamics, horizon=20, dt=0.02)

# Wrap for simulation runner interface
def mpc_wrapper(state, _, __):
    """Adapt MPC to simulation runner interface."""
    t = state['t'] if 't' in state else 0.0
    u = mpc.compute_control(t, state['x'])
    return u, (), {}  # (control, state_vars, history)

# Run simulation
runner = SimulationRunner(config)
result = runner.run(
    controller=mpc_wrapper,
    dynamics=dynamics,
    duration=10.0,
    dt=0.02
)