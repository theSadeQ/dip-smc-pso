# Example from: docs\controllers\classical_smc_technical_guide.md
# Index: 11
# Runnable: True
# Hash: 29318dc7

from src.controllers.smc import ClassicalSMC

# Create controller with specified gains
controller = ClassicalSMC(
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    boundary_layer=0.01,
    switch_method="tanh"
)

# Initialize (stateless for classical SMC)
state_vars = controller.initialize_state()  # Returns ()
history = controller.initialize_history()    # Returns {}

# Main control loop
for t in simulation_time:
    state = get_system_state()  # [x, θ1, θ2, ẋ, θ̇1, θ̇2]

    result = controller.compute_control(state, state_vars, history)

    # Extract results
    control_force = result.control
    history = result.history

    # Apply control
    apply_control(control_force)