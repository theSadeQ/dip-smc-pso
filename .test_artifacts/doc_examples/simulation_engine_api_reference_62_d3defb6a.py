# Example from: docs\api\simulation_engine_api_reference.md
# Index: 62
# Runnable: False
# Hash: d3defb6a

# example-metadata:
# runnable: false

class ResultContainer(ABC):
    """Base interface for simulation result containers."""

    @abstractmethod
    def add_trajectory(self, states: np.ndarray, times: np.ndarray, **metadata) -> None:
        """Add a simulation trajectory to results."""

    @abstractmethod
    def get_states(self) -> np.ndarray:
        """Get state trajectories."""

    @abstractmethod
    def get_times(self) -> np.ndarray:
        """Get time vectors."""

    @abstractmethod
    def export(self, format_type: str, filepath: str) -> None:
        """Export results to specified format."""