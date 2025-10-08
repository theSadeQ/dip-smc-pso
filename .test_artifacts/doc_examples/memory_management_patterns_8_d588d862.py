# Example from: docs\memory_management_patterns.md
# Index: 8
# Runnable: True
# Hash: d588d862

# Cleanup every N iterations
from src.controllers.smc import AdaptiveSMC
import gc

for i in range(10000):
    controller = AdaptiveSMC(
        gains=candidate_gains[i],
        dt=0.01,
        max_force=100,
        k1_init=10,
        k2_init=8,
        gamma1=0.5,
        gamma2=0.5,
        dead_zone=0.01
    )
    fitness = evaluate_controller(controller)

    # Cleanup every 100 iterations
    if i % 100 == 99:
        controller.cleanup()
        del controller
        gc.collect()