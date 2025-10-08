# Example from: docs\guides\api\controllers.md
# Index: 10
# Runnable: False
# Hash: 0396f3c9

# Create super-twisting controller
controller = create_smc_for_pso(
    SMCType.SUPER_TWISTING,
    gains=[25, 10, 15, 12, 20, 15],
    max_force=100.0,
    dt=0.01  # Required for STA integration
)

# STA maintains internal state for integration
state = np.array([0, 0, 0.1, 0, 0.15, 0])
state_vars = {}
history = controller.initialize_history()

# First call initializes integrator
control1, state_vars, history = controller.compute_control(state, state_vars, history)

# Subsequent calls use integrated state
control2, state_vars, history = controller.compute_control(state, state_vars, history)