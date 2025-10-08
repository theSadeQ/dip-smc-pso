# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 11
# Runnable: False
# Hash: a021fb5b

# Duck typing (no type checking)
def simulate_duck(controller):  # No type hint
    u = controller.compute_control(state, {}, {})  # Hope it works!
    return u

# Explicit protocol (type-safe)
def simulate_protocol(controller: ControllerProtocol):
    u, _, _ = controller.compute_control(state, {}, {})  # mypy validates!
    return u

# mypy catches errors at compile time:
# simulate_protocol(None)  # Error: None doesn't implement ControllerProtocol
# simulate_protocol("foo")  # Error: str doesn't implement ControllerProtocol