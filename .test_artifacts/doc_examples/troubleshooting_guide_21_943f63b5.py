# Example from: docs\factory\troubleshooting_guide.md
# Index: 21
# Runnable: False
# Hash: 943f63b5

# example-metadata:
# runnable: false

def fallback_controller_creation(controller_type, gains=None):
    """Fallback controller creation using minimal dependencies."""

    # Minimal controller implementation for emergency use
    class FallbackController:
        def __init__(self, gains):
            self.gains = gains or [10, 8, 6, 4, 20, 2]

        def compute_control(self, state, last_control, history):
            # Simple proportional control as fallback
            error = state[:2]  # Angular errors
            control = -sum(g * e for g, e in zip(self.gains[:2], error))
            return min(max(control, -150), 150)  # Saturate

        def reset(self):
            pass

    print(f"Using fallback controller for {controller_type}")
    return FallbackController(gains)

# Use as last resort
# fallback_controller = fallback_controller_creation('classical_smc')