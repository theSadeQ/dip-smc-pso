# Example from: docs\configuration_integration_documentation.md
# Index: 5
# Runnable: False
# Hash: a1d5b9c6

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Literal

class PhysicsConfig(BaseModel):
    """Physics parameters for the double-inverted pendulum."""

    m1: float = Field(..., gt=0, description="Upper pendulum mass [kg]")
    m2: float = Field(..., gt=0, description="Lower pendulum mass [kg]")
    M: float = Field(..., gt=0, description="Cart mass [kg]")
    l1: float = Field(..., gt=0, description="Upper pendulum length [m]")
    l2: float = Field(..., gt=0, description="Lower pendulum length [m]")
    b1: float = Field(..., ge=0, description="Upper pendulum friction")
    b2: float = Field(..., ge=0, description="Lower pendulum friction")
    I1: float = Field(..., gt=0, description="Upper pendulum inertia [kg⋅m²]")
    I2: float = Field(..., gt=0, description="Lower pendulum inertia [kg⋅m²]")

class SimulationConfig(BaseModel):
    """Simulation parameters."""

    duration: float = Field(..., gt=0, description="Simulation time [s]")
    dt: float = Field(..., gt=0, le=0.01, description="Integration timestep [s]")
    initial_state: List[float] = Field(..., min_items=6, max_items=6)
    use_full_dynamics: bool = Field(False, description="Use full nonlinear dynamics")

    @validator('initial_state')
    def validate_initial_state(cls, v):
        """Validate initial state vector."""
        if len(v) != 6:
            raise ValueError("Initial state must have 6 components")

        # Check angle limits (±π)
        if abs(v[0]) > 3.14159 or abs(v[1]) > 3.14159:
            raise ValueError("Initial angles must be within ±π radians")

        return v

class ClassicalSMCConfig(BaseModel):
    """Classical SMC controller configuration."""

    gains: List[float] = Field(..., min_items=6, max_items=6)
    max_force: float = Field(..., gt=0)
    boundary_layer: float = Field(..., gt=0)
    dt: float = Field(..., gt=0)
    switch_method: Literal["tanh", "linear", "sign"] = "tanh"
    regularization: float = Field(1e-10, gt=0)

    @validator('gains')
    def validate_gains(cls, v):
        """Validate SMC gains for stability."""
        if not all(g > 0 for g in v):
            raise ValueError("All SMC gains must be positive")

        k1, k2, lam1, lam2, K, kd = v

        # Stability constraints
        if lam1 <= 0 or lam2 <= 0:
            raise ValueError("Surface coefficients λ1, λ2 must be positive")

        if K <= 0:
            raise ValueError("Switching gain K must be positive")

        # Practical constraints
        if K > 200:
            raise ValueError("Switching gain K too large (>200), may cause excessive chattering")

        return v

class ConfigSchema(BaseModel):
    """Complete configuration schema."""

    global_seed: Optional[int] = Field(None, ge=0)
    physics: PhysicsConfig
    simulation: SimulationConfig
    controllers: Dict[str, Dict] = Field(default_factory=dict)
    pso: Optional[Dict] = Field(default_factory=dict)
    cost_function: Optional[Dict] = Field(default_factory=dict)
    hil: Optional[Dict] = Field(default_factory=dict)
    logging: Optional[Dict] = Field(default_factory=dict)
    monitoring: Optional[Dict] = Field(default_factory=dict)