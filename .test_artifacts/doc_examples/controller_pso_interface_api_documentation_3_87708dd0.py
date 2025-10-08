# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 3
# Runnable: True
# Hash: 87708dd0

from typing import Dict, Type, Callable
from abc import ABC, abstractmethod

class ControllerFactory:
    """Centralized controller factory with PSO integration."""

    _controller_registry: Dict[str, Callable] = {}

    @classmethod
    def register_controller(cls,
                          name: str,
                          controller_class: Type[PSO_ControllerInterface]) -> None:
        """Register controller class for PSO optimization.

        Parameters
        ----------
        name : str
            Controller identifier (e.g., 'classical_smc')
        controller_class : Type[PSO_ControllerInterface]
            Controller class implementing required interface
        """
        if not hasattr(controller_class, 'max_force'):
            raise TypeError(f"Controller {name} missing required 'max_force' property")

        cls._controller_registry[name] = controller_class

    @classmethod
    def create_controller(cls,
                         controller_type: str,
                         gains: np.ndarray,
                         **kwargs) -> PSO_ControllerInterface:
        """Create controller instance from PSO gains.

        Parameters
        ----------
        controller_type : str
            Registered controller name
        gains : np.ndarray
            PSO-optimized gain vector
        **kwargs
            Additional parameters

        Returns
        -------
        PSO_ControllerInterface
            Configured controller instance
        """
        if controller_type not in cls._controller_registry:
            raise ValueError(f"Unknown controller type: {controller_type}")

        controller_class = cls._controller_registry[controller_type]
        return controller_class(gains, **kwargs)