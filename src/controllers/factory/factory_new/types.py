#======================================================================================\
#===================== src/controllers/factory/factory_new/types.py ===================\
#======================================================================================\

"""
Type definitions, protocols, and constants for the controller factory.

This module provides shared type definitions, protocols, enums, and classes
used across the controller factory modules.

Extracted from monolithic core.py (1,435 lines) during Phase 2 refactor.
"""

# Standard library imports
import logging
import threading
from enum import Enum
from typing import Any, Dict, List, Protocol, Tuple, TypeVar, Union

# Third-party imports
import numpy as np
from numpy.typing import NDArray

# =============================================================================
# MODULE-LEVEL LOGGER
# =============================================================================

logger = logging.getLogger(__name__)

# =============================================================================
# TYPE ALIASES
# =============================================================================

# Type aliases for better type safety
StateVector = NDArray[np.float64]
ControlOutput = Union[float, NDArray[np.float64]]
GainsArray = Union[List[float], NDArray[np.float64]]
ConfigDict = Dict[str, Any]

# Generic type for controller instances
ControllerT = TypeVar('ControllerT')

# =============================================================================
# EXCEPTIONS
# =============================================================================

class ConfigValueError(ValueError):
    """Exception raised for invalid configuration values."""
    pass

# =============================================================================
# PROTOCOLS
# =============================================================================

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

    def reset(self) -> None:
        """Reset controller internal state."""
        ...

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        ...

# =============================================================================
# THREAD SAFETY
# =============================================================================

# Thread-safe factory operations with timeout protection
_factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds

# =============================================================================
# ENUMS
# =============================================================================

class SMCType(Enum):
    """SMC Controller types enumeration."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"

# =============================================================================
# CONFIGURATION CLASSES
# =============================================================================

class SMCConfig:
    """Configuration class for SMC controllers."""
    def __init__(self, gains: List[float], max_force: float = 150.0, dt: float = 0.001, **kwargs: Any) -> None:
        self.gains = gains
        self.max_force = max_force
        self.dt = dt
        for key, value in kwargs.items():
            setattr(self, key, value)

class SMCGainSpec:
    """SMC gain specification with expected interface."""
    def __init__(self, gain_names: List[str], gain_bounds: List[Tuple[float, float]], controller_type: str, n_gains: int):
        self.gain_names = gain_names
        self.gain_bounds = gain_bounds
        self.controller_type = controller_type
        self.n_gains = n_gains

# =============================================================================
# GAIN SPECIFICATIONS
# =============================================================================

SMC_GAIN_SPECS = {
    SMCType.CLASSICAL: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd'],
        gain_bounds=[(1.0, 30.0), (1.0, 30.0), (1.0, 20.0), (1.0, 20.0), (5.0, 50.0), (0.1, 10.0)],
        controller_type='classical_smc',
        n_gains=6
    ),
    SMCType.ADAPTIVE: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'gamma'],
        gain_bounds=[(2.0, 40.0), (2.0, 40.0), (1.0, 25.0), (1.0, 25.0), (0.5, 10.0)],
        controller_type='adaptive_smc',
        n_gains=5
    ),
    SMCType.SUPER_TWISTING: SMCGainSpec(
        gain_names=['K1', 'K2', 'k1', 'k2', 'lambda1', 'lambda2'],
        gain_bounds=[(3.0, 50.0), (2.0, 30.0), (2.0, 30.0), (2.0, 30.0), (0.5, 20.0), (0.5, 20.0)],
        controller_type='sta_smc',
        n_gains=6
    ),
    SMCType.HYBRID: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2'],
        gain_bounds=[(2.0, 30.0), (2.0, 30.0), (1.0, 20.0), (1.0, 20.0)],
        controller_type='hybrid_adaptive_sta_smc',
        n_gains=4
    )
}
