# Example from: docs\api\simulation_engine_api_reference.md
# Index: 44
# Runnable: False
# Hash: 8842b417

class SequentialOrchestrator(BaseOrchestrator):
    """Sequential simulation orchestrator for single-threaded execution."""

    def execute(
        self,
        initial_state: np.ndarray,
        control_inputs: np.ndarray,
        dt: float,
        horizon: int,
        **kwargs
    ) -> ResultContainer:
        """Execute sequential simulation."""