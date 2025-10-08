# Example from: docs\guides\api\controllers.md
# Index: 14
# Runnable: False
# Hash: a3155070

# example-metadata:
# runnable: false

# Create hybrid controller
controller = create_smc_for_pso(
    SMCType.HYBRID,
    gains=[15, 12, 18, 15],  # Only 4 gains
    max_force=100.0,
    dt=0.01
)

# Hybrid combines STA integration with adaptation
state = np.array([0, 0, 0.1, 0, 0.15, 0])
state_vars = {}
history = controller.initialize_history()

control, state_vars, history = controller.compute_control(state, state_vars, history)

# Monitor both STA state and adapted gains
print(f"Control: {control:.2f} N")
print(f"STA state: {state_vars.get('sta_integrator_state', 'N/A')}")
print(f"Adapted gains: {state_vars.get('adapted_gains', 'N/A')}")