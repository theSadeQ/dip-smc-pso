# Example from: docs\technical\controller_factory_integration.md
# Index: 10
# Runnable: True
# Hash: 28aa5c4e

@dataclass
class ControlResult:
    u: float                    # Control action
    sliding_surface: float      # Current sliding surface value
    equivalent_control: float   # Equivalent control component
    switching_control: float    # Switching control component
    controller_state: dict      # Internal controller state