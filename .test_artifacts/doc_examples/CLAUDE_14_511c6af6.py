# Example from: docs\CLAUDE.md
# Index: 14
# Runnable: False
# Hash: 511c6af6

from src.controllers.smc import ClassicalSMC

controller = ClassicalSMC(gains=[...], max_force=100, boundary_layer=0.01)
# ... use controller ...
controller.cleanup()  # Explicit cleanup
del controller