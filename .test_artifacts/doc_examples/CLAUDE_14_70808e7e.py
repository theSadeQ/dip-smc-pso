# Example from: docs\CLAUDE.md
# Index: 14
# Runnable: False
# Hash: 70808e7e

# example-metadata:
# runnable: false

from src.controllers.smc import ClassicalSMC

controller = ClassicalSMC(gains=[...], max_force=100, boundary_layer=0.01)
# ... use controller ...
controller.cleanup()  # Explicit cleanup
del controller