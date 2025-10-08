# Example from: docs\guides\api\controllers.md
# Index: 12
# Runnable: False
# Hash: 2c56d8da

# example-metadata:
# runnable: false

# Create adaptive controller
controller = create_smc_for_pso(
    SMCType.ADAPTIVE,
    gains=[10, 8, 15, 12, 0.5],  # Only 5 gains
    max_force=100.0
)

# Adaptive SMC tracks gain evolution
state = np.array([0, 0, 0.1, 0, 0.15, 0])
state_vars = {}
history = controller.initialize_history()

# Gains adapt during simulation
for i in range(1000):
    control, state_vars, history = controller.compute_control(state, state_vars, history)

    # Monitor adapted gains
    if 'adapted_gains' in state_vars:
        print(f"Step {i}: Adapted gains = {state_vars['adapted_gains']}")