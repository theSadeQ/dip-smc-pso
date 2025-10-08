# Example from: docs\factory\factory_api_reference.md
# Index: 7
# Runnable: False
# Hash: 74f68610

# example-metadata:
# runnable: false

class ControllerProtocol(Protocol):
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