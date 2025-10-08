# Example from: docs\controllers\control_primitives_reference.md
# Index: 10
# Runnable: True
# Hash: bde16bb9

from src.controllers.adaptive_smc import AdaptiveSMC

controller = AdaptiveSMC(gains=[25, 18, 15, 10, 4], dt=0.01, max_force=100)
result = controller.compute_control(state, (), {})

# Monitor sliding surface convergence
if abs(result.sigma) < 0.01:
    print("Reached sliding surface")