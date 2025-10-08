# Example from: docs\PATTERNS.md
# Index: 17
# Runnable: False
# Hash: 6ab7ef13

# src/controllers/factory.py (lines 95-102)

from typing import Any, Callable, Dict, List, Optional, Union, Protocol
from numpy.typing import NDArray
import numpy as np

# Type aliases for clarity
StateVector = NDArray[np.float64]
ControlOutput = Union[float, NDArray[np.float64]]
GainsArray = Union[List[float], NDArray[np.float64]]
ConfigDict = Dict[str, Any]

def create_controller(controller_type: str,
                     config: Optional[Any] = None,
                     gains: Optional[GainsArray] = None) -> ControllerProtocol:
    """Type-safe controller instantiation."""
    ...