# Example from: docs\api\factory_system_api_reference.md
# Index: 6
# Runnable: False
# Hash: bfc9acf5

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