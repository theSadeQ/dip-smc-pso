# Example from: docs\controllers\control_primitives_reference.md
# Index: 12
# Runnable: True
# Hash: 7eeeed33

from src.controllers.sta_smc import SuperTwistingSMC

controller = SuperTwistingSMC(gains=[25, 15, 20, 12, 8, 6], dt=0.01, max_force=100)

# Initialize state
z_prev, sigma_prev = 0.0, 0.0

for t, state in simulation_loop:
    result = controller.compute_control(state, (z_prev, sigma_prev), {})
    u = result.u
    z_prev, sigma_prev = result.state  # Update auxiliary states