# Example from: docs\technical\integration_protocols.md
# Index: 3
# Runnable: False
# Hash: 9884374f

class ControllerPlantBridge:
    """Bridge for controller-plant communication."""

    def __init__(self, controller, plant_model):
        self.controller = controller
        self.plant_model = plant_model
        self._validate_compatibility()

    def _validate_compatibility(self):
        """Validate controller-plant compatibility."""
        # Check state dimensions
        controller_states = getattr(self.controller, 'expected_states', 6)
        plant_states = self.plant_model.state_dimension

        if controller_states != plant_states:
            raise ValueError(
                f"State dimension mismatch: controller expects {controller_states}, "
                f"plant provides {plant_states}"
            )

        # Check control dimensions
        controller_controls = getattr(self.controller, 'control_dimension', 1)
        plant_controls = self.plant_model.control_dimension

        if controller_controls != plant_controls:
            raise ValueError(
                f"Control dimension mismatch: controller outputs {controller_controls}, "
                f"plant expects {plant_controls}"
            )

    def step(self, state: np.ndarray, dt: float) -> Tuple[np.ndarray, dict]:
        """Execute one control-plant step."""
        # Validate state
        if not self.plant_model.validate_state(state):
            raise ValueError("Invalid state for plant model")

        # Compute control
        control_result = self.controller.compute_control(state, (), {})
        u = control_result.u if hasattr(control_result, 'u') else control_result

        # Apply control to plant
        state_derivative = self.plant_model.compute_dynamics(state, u)

        # Integrate (simple Euler for demonstration)
        next_state = state + dt * state_derivative

        # Collect metadata
        metadata = {
            'control_value': u,
            'sliding_surface': getattr(control_result, 'sliding_surface', None),
            'plant_model': type(self.plant_model).__name__,
            'controller_type': type(self.controller).__name__
        }

        return next_state, metadata