# Example from: docs\technical\integration_protocols.md
# Index: 1
# Runnable: True
# Hash: c240e7bb

from abc import ABC, abstractmethod
from typing import Tuple, Optional
import numpy as np

class PlantModelInterface(ABC):
    """Standard interface for plant models in the factory ecosystem."""

    @abstractmethod
    def compute_dynamics(
        self,
        state: np.ndarray,
        control: float,
        disturbances: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Compute system dynamics: dx/dt = f(x, u, d)

        Parameters
        ----------
        state : np.ndarray, shape (6,)
            Current system state [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
        control : float
            Control input (cart force)
        disturbances : np.ndarray, optional
            External disturbances

        Returns
        -------
        np.ndarray, shape (6,)
            State derivative vector
        """
        pass

    @abstractmethod
    def get_linearization(
        self,
        state: np.ndarray,
        control: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get linearized dynamics around operating point.

        Returns
        -------
        A : np.ndarray, shape (6, 6)
            State matrix
        B : np.ndarray, shape (6, 1)
            Input matrix
        """
        pass

    @abstractmethod
    def validate_state(self, state: np.ndarray) -> bool:
        """Validate if state is within acceptable bounds."""
        pass

    @property
    @abstractmethod
    def state_dimension(self) -> int:
        """Return the state space dimension."""
        pass

    @property
    @abstractmethod
    def control_dimension(self) -> int:
        """Return the control input dimension."""
        pass