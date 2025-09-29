#======================================================================================\\\
#===================== src/controllers/factory/core/protocols.py ======================\\\
#======================================================================================\\\

"""
Core Protocols and Interfaces for Controller Factory

Defines the fundamental protocols and interfaces that all controllers and factory
components must adhere to for type safety and consistency.
"""

from typing import Protocol, Any, Dict, List, Optional, Union
import numpy as np
from numpy.typing import NDArray

# Type aliases for better readability
StateVector = NDArray[np.float64]
ControlOutput = Union[float, NDArray[np.float64]]
GainsArray = Union[List[float], NDArray[np.float64]]
ConfigDict = Dict[str, Any]


class ControllerProtocol(Protocol):
    """Protocol defining the standard controller interface."""

    def compute_control(
        self,
        state: StateVector,
        last_control: float,
        history: ConfigDict
    ) -> ControlOutput:
        """Compute control output for given state.

        Args:
            state: Current system state vector
            last_control: Previous control input
            history: Historical data for controller

        Returns:
            Control output value
        """
        ...

    def reset(self) -> None:
        """Reset controller internal state."""
        ...

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        ...

    @property
    def max_force(self) -> float:
        """Return maximum force limit."""
        ...


class ConfigurationProtocol(Protocol):
    """Protocol for controller configuration objects."""

    @property
    def gains(self) -> List[float]:
        """Controller gains."""
        ...

    @property
    def max_force(self) -> float:
        """Maximum force limit."""
        ...

    @property
    def dt(self) -> float:
        """Time step."""
        ...


class ControllerFactoryProtocol(Protocol):
    """Protocol for controller factory functions."""

    def create_controller(
        self,
        controller_type: str,
        config: Optional[Any] = None,
        gains: Optional[GainsArray] = None
    ) -> ControllerProtocol:
        """Create a controller instance.

        Args:
            controller_type: Type of controller to create
            config: Configuration object
            gains: Controller gains

        Returns:
            Configured controller instance
        """
        ...

    def list_available_controllers(self) -> List[str]:
        """List available controller types."""
        ...

    def get_default_gains(self, controller_type: str) -> List[float]:
        """Get default gains for controller type."""
        ...


class PSOOptimizableProtocol(Protocol):
    """Protocol for PSO-optimizable controllers."""

    def compute_control(self, state: StateVector) -> NDArray[np.float64]:
        """Compute control output for PSO optimization.

        Args:
            state: System state vector

        Returns:
            Control output as numpy array
        """
        ...

    @property
    def n_gains(self) -> int:
        """Number of optimization parameters."""
        ...

    @property
    def controller_type(self) -> str:
        """Controller type identifier."""
        ...

    @property
    def max_force(self) -> float:
        """Maximum force limit."""
        ...


class ValidationProtocol(Protocol):
    """Protocol for validation functions."""

    def validate_gains(
        self,
        gains: GainsArray,
        controller_type: str
    ) -> Dict[str, Any]:
        """Validate controller gains.

        Args:
            gains: Gains to validate
            controller_type: Type of controller

        Returns:
            Validation results
        """
        ...

    def validate_configuration(
        self,
        config: Any,
        controller_type: str
    ) -> Dict[str, Any]:
        """Validate configuration object.

        Args:
            config: Configuration to validate
            controller_type: Type of controller

        Returns:
            Validation results
        """
        ...