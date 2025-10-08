# Example from: docs\memory_management_quick_reference.md
# Index: 2
# Runnable: True
# Hash: f8606b49

from src.controllers.smc import HybridAdaptiveSTASMC
import gc
import time

controller = HybridAdaptiveSTASMC(
    gains=[15, 12, 18, 15],
    dt=0.01,
    max_force=100,
    k1_init=10,
    k2_init=8,
    gamma1=0.5,
    gamma2=0.5,
    dead_zone=0.01
)

history = controller.initialize_history()
state_vars = controller.initialize_state()
last_cleanup = time.time()

while running:
    control, state_vars, history = controller.compute_control(state, state_vars, history)

    # Hourly cleanup
    if time.time() - last_cleanup > 3600:
        history = controller.initialize_history()
        gc.collect()
        last_cleanup = time.time()

    # Memory monitoring (optional)
    memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
    if memory_mb > 500:
        logger.warning(f"High memory usage: {memory_mb:.1f}MB")
        history = controller.initialize_history()
        gc.collect()