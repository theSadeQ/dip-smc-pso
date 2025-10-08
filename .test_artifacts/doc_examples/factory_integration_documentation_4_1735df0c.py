# Example from: docs\factory_integration_documentation.md
# Index: 4
# Runnable: False
# Hash: 1735df0c

class ControllerProtocol(Protocol):
    """Protocol defining the standard controller interface."""

    def compute_control(
        self,
        state: StateVector,
        last_control: float,
        history: ConfigDict
    ) -> ControlOutput:
        """Compute control output for given state."""
        ...

    def reset(self) -> None:
        """Reset controller internal state."""
        ...

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        ...