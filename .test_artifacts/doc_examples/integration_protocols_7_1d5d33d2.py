# Example from: docs\technical\integration_protocols.md
# Index: 7
# Runnable: False
# Hash: 1d5d33d2

# example-metadata:
# runnable: false

class RealTimeSimulationBridge:
    """Bridge for real-time simulation integration."""

    def __init__(self, controller, dt: float = 0.001):
        self.controller = controller
        self.dt = dt
        self.last_control = 0.0
        self.control_history = {}

    def real_time_step(self, state: np.ndarray, timestamp: float) -> float:
        """Execute real-time control step."""
        try:
            # Compute control with timing constraints
            start_time = time.perf_counter()

            control_result = self.controller.compute_control(
                state,
                self.last_control,
                self.control_history
            )

            computation_time = time.perf_counter() - start_time

            # Extract control value
            u = control_result.u if hasattr(control_result, 'u') else control_result

            # Update state
            self.last_control = u
            self.control_history[timestamp] = {
                'control': u,
                'computation_time': computation_time,
                'state': state.copy()
            }

            # Validate real-time constraints
            if computation_time > self.dt:
                logger.warning(
                    f"Control computation time {computation_time:.6f}s "
                    f"exceeds timestep {self.dt:.6f}s"
                )

            return u

        except Exception as e:
            logger.error(f"Real-time control step failed: {e}")
            return self.last_control  # Use last valid control