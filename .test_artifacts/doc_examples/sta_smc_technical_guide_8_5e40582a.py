# Example from: docs\controllers\sta_smc_technical_guide.md
# Index: 8
# Runnable: True
# Hash: 5e40582a

from src.controllers.smc import SuperTwistingSMC

# Create controller (6 gains)
controller = SuperTwistingSMC(
    gains=[25.0, 15.0, 10.0, 8.0, 15.0, 12.0],
    dt=0.01,
    max_force=150.0,
    damping_gain=3.0,
    boundary_layer=0.01
)

# OR minimal (2 gains with defaults)
controller = SuperTwistingSMC(
    gains=[25.0, 15.0],
    dt=0.01,
    max_force=150.0
)

# Initialize
state_vars = controller.initialize_state()  # (0.0, 0.0)
history = controller.initialize_history()

# Main loop
for t in simulation_time:
    state = get_system_state()

    result = controller.compute_control(state, state_vars, history)

    control_force = result.control
    state_vars = result.state_vars  # (z_new, sigma)
    history = result.history

    apply_control(control_force)