# Example from: docs\memory_management_quick_reference.md
# Index: 3
# Runnable: True
# Hash: ccc33e42

from src.controllers.smc import AdaptiveSMC
import gc

for i in range(10000):
    controller = AdaptiveSMC(
        gains=candidates[i],
        dt=0.01,
        max_force=100,
        k1_init=10,
        k2_init=8,
        gamma1=0.5,
        gamma2=0.5,
        dead_zone=0.01
    )
    fitness[i] = evaluate(controller)

    if i % 100 == 99:
        controller.cleanup()
        del controller
        gc.collect()