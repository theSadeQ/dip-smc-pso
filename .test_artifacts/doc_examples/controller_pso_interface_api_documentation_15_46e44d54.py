# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 15
# Runnable: False
# Hash: 46e44d54

# example-metadata:
# runnable: false

class PSO_ControllerError(Exception):
    """Base exception for PSO-controller interface errors."""
    pass

class InvalidGainsError(PSO_ControllerError):
    """Raised when gain vector is invalid."""
    def __init__(self, gains: np.ndarray, controller_type: str, reason: str):
        self.gains = gains
        self.controller_type = controller_type
        self.reason = reason
        super().__init__(f"Invalid gains for {controller_type}: {reason}")

class ControllerInstantiationError(PSO_ControllerError):
    """Raised when controller creation fails."""
    pass

class SimulationError(PSO_ControllerError):
    """Raised when control simulation fails."""
    pass