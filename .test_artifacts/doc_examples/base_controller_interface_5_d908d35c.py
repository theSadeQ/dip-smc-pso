# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 5
# Runnable: True
# Hash: d908d35c

# No type checking - relies on runtime behavior
def simulate(controller):
    u = controller.compute_control(state, {}, {})  # Hope it works!