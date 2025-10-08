# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 17
# Runnable: True
# Hash: 7ad22736

from time import perf_counter
from dataclasses import dataclass, field
from typing import List

@dataclass
class PerformanceMetrics:
    """Controller performance metrics."""
    creation_time: float = 0.0
    control_computation_times: List[float] = field(default_factory=list)
    memory_usage: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0

    @property
    def mean_control_time(self) -> float:
        """Mean control computation time."""
        return np.mean(self.control_computation_times) if self.control_computation_times else 0.0

    @property
    def max_control_time(self) -> float:
        """Maximum control computation time."""
        return np.max(self.control_computation_times) if self.control_computation_times else 0.0

class PerformanceMonitoredController:
    """Wrapper for performance monitoring."""

    def __init__(self, controller: PSO_ControllerInterface):
        self.controller = controller
        self.metrics = PerformanceMetrics()
        self._creation_start = perf_counter()

    def __getattr__(self, name):
        """Delegate attribute access to wrapped controller."""
        return getattr(self.controller, name)

    def compute_control(self, state: np.ndarray, **kwargs) -> float:
        """Timed control computation."""
        start_time = perf_counter()
        result = self.controller.compute_control(state, **kwargs)
        end_time = perf_counter()

        self.metrics.control_computation_times.append(end_time - start_time)
        return result