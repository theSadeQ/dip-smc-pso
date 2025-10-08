# Example from: docs\implementation\legacy_code_documentation_index.md
# Index: 2
# Runnable: False
# Hash: 92935b70

# example-metadata:
# runnable: false

from typing import Protocol, Optional, Tuple
from pydantic import BaseModel, validator, Field
import numpy as np

class ControllerProtocol(Protocol):
    """Protocol defining the controller interface."""

    def compute_control(
        self,
        x: np.ndarray,
        x_ref: np.ndarray,
        t: float
    ) -> float:
        """Compute control input with guaranteed interface."""
        ...

class SMCParameters(BaseModel):
    """Validated SMC parameters with mathematical constraints."""

    c: List[float] = Field(..., description="Sliding surface gains")
    eta: float = Field(gt=0, description="Switching gain")
    epsilon: float = Field(gt=0, lt=1, description="Boundary layer")

    @validator('c')
    def validate_sliding_gains(cls, v):
        if not all(ci > 0 for ci in v):
            raise ValueError("All sliding gains must be positive")
        return v

    @validator('eta')
    def validate_switching_gain(cls, v, values):
        # Theoretical lower bound from uncertainty analysis
        if v < 0.1:
            raise ValueError("Switching gain too small for robustness")
        return v