# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 12
# Runnable: True
# Hash: 480c1e9c

# Base class behavior
from src.controllers.base import Controller

def reset_controller(controller: Controller):
    """Works with any Controller subclass."""
    history = controller.reset()
    return history

# Works for all subclasses
classical = ClassicalSMC(gains=[10, 8, 15, 12, 50, 0.01])
adaptive = AdaptiveSMC(gains=[10, 8, 15, 12, 0.5])

history_classical = reset_controller(classical)  # Works
history_adaptive = reset_controller(adaptive)    # Works

# Substitutability guaranteed by LSP