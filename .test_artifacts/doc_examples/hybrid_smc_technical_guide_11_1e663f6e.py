# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 11
# Runnable: True
# Hash: 1e663f6e

from src.controllers.smc import HybridAdaptiveSTASMC

# Create controller with optimized gains
controller = HybridAdaptiveSTASMC(
    gains=[77.6216, 44.449, 17.3134, 14.25],
    dt=0.01,
    max_force=100.0,
    k1_init=2.0,
    k2_init=1.0,
    gamma1=0.5,
    gamma2=0.3,
    dead_zone=0.01
)

# Initialize controller state
state_vars = controller.initialize_state()
history = controller.initialize_history()

# Main control loop
for t in simulation_time:
    state = get_system_state()  # [x, θ1, θ2, ẋ, θ̇1, θ̇2]

    result = controller.compute_control(state, state_vars, history)

    # Extract results
    control_force = result.control
    state_vars = result.state_vars  # (k1, k2, u_int)
    history = result.history
    sliding_surface = result.sliding_surface

    # Apply control to system
    apply_control(control_force)