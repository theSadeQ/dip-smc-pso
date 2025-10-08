# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 6
# Runnable: True
# Hash: 9ccfdec1

def simulate(controller: ControllerProtocol):
    u = controller.compute_control(state, {}, {})  # Type-safe!