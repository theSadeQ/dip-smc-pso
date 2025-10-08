# Example from: docs\pso_integration_system_architecture.md
# Index: 5
# Runnable: False
# Hash: 48d72243

# example-metadata:
# runnable: false

class ControllerInterface:
    def __init__(self, gains: np.ndarray):
        """Initialize with gain vector from PSO particle."""

    @property
    def max_force(self) -> float:
        """Actuator saturation limit for simulation."""

    def validate_gains(self, particles: np.ndarray) -> np.ndarray:
        """Optional: Pre-filter invalid particles (returns boolean mask)."""

    def compute_control(self, state: np.ndarray, **kwargs) -> float:
        """Required: Control law implementation."""