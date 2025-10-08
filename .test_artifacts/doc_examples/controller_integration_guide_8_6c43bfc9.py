# Example from: docs\factory\controller_integration_guide.md
# Index: 8
# Runnable: True
# Hash: 6c43bfc9

class PSOControllerWrapper:
    """
    Enhanced wrapper for PSO optimization integration.

    Features:
    - Simplified control interface for PSO fitness functions
    - Automatic gain validation
    - Performance monitoring
    - Thread-safe operation
    """

    def __init__(
        self,
        controller: ControllerProtocol,
        controller_type: str,
        validation_enabled: bool = True
    ):
        self.controller = controller
        self.controller_type = controller_type
        self.validation_enabled = validation_enabled
        self.n_gains = self._determine_gain_count()
        self.max_force = getattr(controller, 'max_force', 150.0)

        # Performance monitoring
        self.call_count = 0
        self.total_compute_time = 0.0
        self.max_control_magnitude = 0.0

    def _determine_gain_count(self) -> int:
        """Determine expected gain count for controller type."""
        gain_counts = {
            'classical_smc': 6,
            'adaptive_smc': 5,
            'sta_smc': 6,
            'hybrid_adaptive_sta_smc': 4
        }
        return gain_counts.get(self.controller_type, 6)

    def compute_control(
        self,
        state: StateVector,
        return_metadata: bool = False
    ) -> Union[NDArray[np.float64], Tuple[NDArray[np.float64], Dict[str, Any]]]:
        """
        PSO-optimized control computation with optional metadata.

        Args:
            state: System state vector [θ1, θ2, x, θ̇1, θ̇2, ẋ]
            return_metadata: Whether to return computation metadata

        Returns:
            Control output as numpy array, optionally with metadata
        """
        import time

        start_time = time.time()

        try:
            # Validate input state
            if len(state) != 6:
                raise ValueError(f"Expected 6-DOF state, got {len(state)}")

            # Compute control using full controller interface
            result = self.controller.compute_control(state, (), {})

            # Extract control value
            if hasattr(result, 'u'):
                control_value = result.u
            elif isinstance(result, dict) and 'u' in result:
                control_value = result['u']
            else:
                control_value = result

            # Convert to numpy array
            if isinstance(control_value, (int, float)):
                control_array = np.array([float(control_value)])
            elif isinstance(control_value, np.ndarray):
                control_array = control_value.flatten()
            else:
                control_array = np.array([float(control_value)])

            # Apply safety saturation
            control_array = np.clip(control_array, -self.max_force, self.max_force)

            # Update performance metrics
            compute_time = time.time() - start_time
            self.call_count += 1
            self.total_compute_time += compute_time
            self.max_control_magnitude = max(self.max_control_magnitude, np.abs(control_array[0]))

            if return_metadata:
                metadata = {
                    'compute_time': compute_time,
                    'call_count': self.call_count,
                    'avg_compute_time': self.total_compute_time / self.call_count,
                    'max_control_magnitude': self.max_control_magnitude,
                    'saturation_applied': np.abs(control_value) > self.max_force
                }
                return control_array, metadata
            else:
                return control_array

        except Exception as e:
            logger.error(f"Control computation failed: {e}")
            # Return safe zero control
            if return_metadata:
                return np.array([0.0]), {'error': str(e)}
            else:
                return np.array([0.0])

    def validate_gains(self, gains: GainsArray) -> bool:
        """Validate gains for PSO optimization."""
        if not self.validation_enabled:
            return True

        try:
            gains_array = np.asarray(gains)

            # Check length
            if len(gains_array) != self.n_gains:
                return False

            # Check for finite positive values
            if not np.all(np.isfinite(gains_array)):
                return False

            if not np.all(gains_array > 0):
                return False

            # Controller-specific validation
            if self.controller_type == 'adaptive_smc':
                gamma = gains_array[4]
                if gamma > 10.0 or gamma < 0.01:
                    return False

            return True

        except Exception:
            return False

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for optimization analysis."""
        return {
            'total_calls': self.call_count,
            'total_compute_time': self.total_compute_time,
            'avg_compute_time': self.total_compute_time / max(1, self.call_count),
            'max_control_magnitude': self.max_control_magnitude,
            'real_time_compatible': self.total_compute_time / max(1, self.call_count) < 0.001
        }