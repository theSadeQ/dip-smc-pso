# Example from: docs\memory_management_quick_reference.md
# Index: 1
# Runnable: True
# Hash: 8e915751

from src.controllers.smc import ClassicalSMC

controller = ClassicalSMC(
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100,
    boundary_layer=0.01
)
result = simulate(controller, duration=5.0)
# Done - automatic cleanup