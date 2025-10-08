# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 12
# Runnable: False
# Hash: 699eb67e

class SlidingSurface(ABC):
    """Abstract interface for sliding surface calculations."""

    @abstractmethod
    def compute(self, state: np.ndarray) -> float:
        """Compute sliding surface value."""
        pass

    @abstractmethod
    def compute_derivative(self, state: np.ndarray, state_dot: np.ndarray) -> float:
        """Compute sliding surface derivative."""
        pass

    @abstractmethod
    def _validate_gains(self) -> None:
        """Validate gains for mathematical correctness."""
        pass

class BoundaryLayer:
    """Interface for boundary layer implementations."""

    def compute_switching_function(self, surface_value: float) -> float:
        """Compute continuous switching function."""
        pass

    def compute_switching_control(self, surface_value: float, gain: float, surface_derivative: float = 0.0) -> float:
        """Compute switching control with boundary layer."""
        pass