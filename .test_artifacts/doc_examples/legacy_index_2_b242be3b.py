# Example from: docs\implementation\legacy_index.md
# Index: 2
# Runnable: False
# Hash: b242be3b

# example-metadata:
# runnable: false

from typing import Protocol, TypeVar, Generic
from pydantic import BaseModel, validator

class ControllerProtocol(Protocol):
    """Protocol defining controller interface."""

    def compute_control(
        self,
        x: np.ndarray,
        x_ref: np.ndarray,
        t: float
    ) -> float:
        """Compute control input."""
        ...

class SimulationConfig(BaseModel):
    """Validated simulation configuration."""

    duration: float = Field(gt=0, description="Simulation duration")
    dt: float = Field(gt=0, lt=0.1, description="Time step")

    @validator('dt')
    def dt_stability(cls, v, values):
        if 'duration' in values and v > values['duration'] / 100:
            raise ValueError("Time step too large for stability")
        return v