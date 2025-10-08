# Example from: docs\controllers\adaptive_smc_technical_guide.md
# Index: 8
# Runnable: True
# Hash: 5873274b

from src.controllers.smc import AdaptiveSMC

# Create controller
controller = AdaptiveSMC(
    gains=[10.0, 8.0, 15.0, 12.0, 0.5],
    dt=0.01,
    max_force=100.0,
    leak_rate=0.001,
    adapt_rate_limit=10.0,
    K_min=0.1,
    K_max=100.0,
    smooth_switch=True,
    boundary_layer=0.01,
    dead_zone=0.01,
    K_init=10.0,
    alpha=0.5
)

# Initialize state and history
state_vars = controller.initialize_state()  # (K_init, 0.0, 0.0)
history = controller.initialize_history()

# Main control loop
for t in simulation_time:
    state = get_system_state()  # [x, θ1, θ2, ẋ, θ̇1, θ̇2]

    result = controller.compute_control(state, state_vars, history)

    # Extract results
    control_force = result.control
    state_vars = result.state_vars  # (K_new, u, time_in_sliding)
    history = result.history
    sigma = result.sliding_surface

    # Monitor adaptation
    current_K = state_vars[0]
    print(f"Adaptive gain: K = {current_K:.2f}")

    # Apply control
    apply_control(control_force)