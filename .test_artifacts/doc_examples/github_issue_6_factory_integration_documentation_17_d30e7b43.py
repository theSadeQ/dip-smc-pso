# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 17
# Runnable: False
# Hash: d30e7b43

# example-metadata:
# runnable: false

class PSOControllerWrapper:
    """
    PSO-optimized wrapper for SMC controllers.

    Provides simplified interface for PSO fitness evaluation:
    - Single-parameter control computation
    - Automatic state management
    - Unified output format
    - Error handling for robustness

    Methods:
        compute_control: Simplified control computation
        gains: Access to controller gains
    """

    def __init__(self, controller: SMCProtocol):
        """Initialize wrapper with SMC controller."""

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """
        Compute control with simplified interface.

        Args:
            state: System state [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]

        Returns:
            Control output as numpy array [u]
        """

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""