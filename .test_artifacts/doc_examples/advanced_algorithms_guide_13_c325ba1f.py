# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 13
# Runnable: True
# Hash: c325ba1f

from src.controllers.smc import ClassicalSMC

# Create controller pool
pool_size = 100
controller_pool = [
    ClassicalSMC(gains=default_gains, max_force=100, boundary_layer=0.01)
    for _ in range(pool_size)
]

# Reuse controllers (update gains instead of creating new instances)
for iteration in range(pso_iterations):
    for i, gains in enumerate(swarm_positions):
        controller = controller_pool[i % pool_size]
        controller.set_gains(gains)  # Update in-place
        cost = evaluate(controller)

# Explicit cleanup after optimization
for controller in controller_pool:
    controller.cleanup()