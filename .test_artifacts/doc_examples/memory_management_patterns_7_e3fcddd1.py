# Example from: docs\memory_management_patterns.md
# Index: 7
# Runnable: True
# Hash: e3fcddd1

# Explicit cleanup recommended
from src.controllers.smc import HybridAdaptiveSTASMC
import gc
import time

controller = HybridAdaptiveSTASMC(
    gains=[15,12,18,15],
    dt=0.01,
    max_force=100,
    k1_init=10,
    k2_init=8,
    gamma1=0.5,
    gamma2=0.5,
    dead_zone=0.01
)

last_cleanup = time.time()

try:
    while server_running:
        state = get_state()
        control, state_vars, history = controller.compute_control(state, last_state_vars, history)
        apply_control(control)

        # Periodic cleanup (every hour)
        if time.time() - last_cleanup > 3600:
            # Clear history buffers to prevent unbounded growth
            history = controller.initialize_history()
            gc.collect()
            last_cleanup = time.time()
finally:
    controller.cleanup()  # Explicit cleanup before deletion
    del controller