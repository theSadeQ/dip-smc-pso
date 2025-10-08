# Example from: docs\guides\api\plant-models.md
# Index: 8
# Runnable: False
# Hash: 05fca37b

# example-metadata:
# runnable: false

class DisturbedDynamics(FullDynamics):
    """Dynamics with external disturbance."""

    def __init__(self, params, disturbance_magnitude=10.0):
        super().__init__(params)
        self.disturbance_magnitude = disturbance_magnitude

    def compute_dynamics(self, state, control, time=0.0):
        """Add time-varying disturbance."""
        # Sinusoidal disturbance
        disturbance = self.disturbance_magnitude * np.sin(2 * np.pi * time)

        # Apply to control
        disturbed_control = control + disturbance

        return super().compute_dynamics(state, disturbed_control)