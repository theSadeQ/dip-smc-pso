# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 11
# Runnable: True
# Hash: 53186df2

from src.controllers.factory import SMCType, create_controller

# Create classical SMC controller
controller = create_controller(
    ctrl_type=SMCType.CLASSICAL,
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 0.01],
    max_force=100.0,
    dt=0.01
)

# Use controller
state = np.array([0.1, 0.0, 0.05, 0.1, 0.02, 0.05])
u, state_vars, history = controller.compute_control(state, {}, {})
print(f"Control output: {u:.2f} N")