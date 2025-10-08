# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 1
# Runnable: False
# Hash: 155aeb85

# example-metadata:
# runnable: false

from typing import Protocol
import numpy as np

class SMCProtocol(Protocol):
    """Type-safe protocol for all SMC controllers."""

    def compute_control(self,
                       state: np.ndarray,
                       state_vars: Any,
                       history: Dict[str, Any]) -> Any:
        """Compute control input for given state."""
        ...

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        ...