# Example from: docs\reports\factory_code_beautification_report.md
# Index: 4
# Runnable: False
# Hash: ed20fc76

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