# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 16
# Runnable: False
# Hash: bfd3304e

class SimulationContext:
    """Centralized simulation state and configuration."""

    state: np.ndarray           # Current state [6,]
    time: float                 # Current time
    controller_vars: Dict       # Controller internal state
    dynamics_params: Dict       # Physics parameters
    history: StateHistory       # Trajectory recording

    def update(self, x_next, u, dt):
        """Thread-safe state update."""
        with self._lock:
            self.state = x_next
            self.time += dt
            self.history.append(self.state, u)