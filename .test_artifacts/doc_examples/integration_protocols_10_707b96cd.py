# Example from: docs\technical\integration_protocols.md
# Index: 10
# Runnable: True
# Hash: 707b96cd

from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np

@dataclass
class SystemState:
    """Standard system state representation."""
    timestamp: float
    state_vector: np.ndarray  # [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ControlAction:
    """Standard control action representation."""
    timestamp: float
    control_value: float
    controller_state: Optional[Dict[str, Any]] = None
    computation_time: Optional[float] = None

@dataclass
class SimulationResult:
    """Standard simulation result representation."""
    timestamps: np.ndarray
    states: np.ndarray
    controls: np.ndarray
    performance_metrics: Dict[str, float]
    metadata: Dict[str, Any]

@dataclass
class OptimizationResult:
    """Standard optimization result representation."""
    optimal_gains: List[float]
    optimal_cost: float
    convergence_history: List[float]
    optimization_metadata: Dict[str, Any]