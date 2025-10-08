# Example from: docs\memory_management_patterns.md
# Index: 6
# Runnable: True
# Hash: eaebbf22

# No explicit cleanup needed (automatic via __del__)
from src.controllers.smc import ClassicalSMC

controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100, boundary_layer=0.01)
results = simulate(controller, duration=5.0)
# Controller automatically cleaned up when out of scope