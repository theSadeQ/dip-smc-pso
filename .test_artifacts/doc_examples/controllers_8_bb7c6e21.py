# Example from: docs\guides\api\controllers.md
# Index: 8
# Runnable: True
# Hash: bb7c6e21

from src.controllers import create_smc_for_pso, SMCType
import numpy as np

# Create controller
controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)

# Compute control
state = np.array([0, 0, 0.1, 0, 0.15, 0])  # [x, dx, θ₁, dθ₁, θ₂, dθ₂]
state_vars = {}
history = controller.initialize_history()

control, state_vars, history = controller.compute_control(state, state_vars, history)
print(f"Control force: {control:.2f} N")