# Example from: docs\PATTERNS.md
# Index: 13
# Runnable: False
# Hash: 89cd4f7b

# src/controllers/factory.py (lines 114-134)

class ControllerProtocol(Protocol):
    """Minimal controller interface - only essential methods."""

    def compute_control(self, state: StateVector, last_control: float,
                       history: ConfigDict) -> ControlOutput:
        """Compute control output for given state."""
        ...

    def reset(self) -> None:
        """Reset controller internal state."""
        ...

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        ...