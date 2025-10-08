# Example from: docs\api\simulation_engine_api_reference.md
# Index: 43
# Runnable: False
# Hash: 40f0cdf2

# example-metadata:
# runnable: false

class Orchestrator(ABC):
    """Base interface for simulation execution strategies."""

    @abstractmethod
    def execute(
        self,
        initial_state: np.ndarray,
        control_inputs: np.ndarray,
        dt: float,
        horizon: int,
        **kwargs
    ) -> ResultContainer:
        """Execute simulation with specified strategy."""
        pass