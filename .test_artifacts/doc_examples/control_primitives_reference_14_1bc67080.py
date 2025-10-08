# Example from: docs\controllers\control_primitives_reference.md
# Index: 14
# Runnable: True
# Hash: 1bc67080

from src.controllers.hybrid_adaptive_sta_smc import HybridAdaptiveSTASMC

controller = HybridAdaptiveSTASMC(
    gains=[18, 12, 10, 8],
    dt=0.01,
    max_force=100,
    k1_init=5.0,
    k2_init=3.0
)

# Initialize adaptive state
k1, k2, u_int = controller.k1_init, controller.k2_init, 0.0

for t, state in simulation_loop:
    result = controller.compute_control(state, (k1, k2, u_int), {})
    u = result.u
    k1, k2, u_int = result.state  # Update adaptive gains