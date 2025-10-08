# Example from: docs\reports\factory_code_beautification_report.md
# Index: 4
# Runnable: False
# Hash: 7c088058

# example-metadata:
# runnable: false

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