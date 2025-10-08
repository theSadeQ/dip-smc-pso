# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 23
# Runnable: False
# Hash: 92343442

# tests/utils/error_injection.py

class ErrorInjector:
    """Inject errors for fault tolerance testing."""

    @staticmethod
    def inject_nan(state, probability=0.1):
        """Randomly inject NaN values into state."""
        mask = np.random.random(state.shape) < probability
        corrupted = state.copy()
        corrupted[mask] = np.nan
        return corrupted

    @staticmethod
    def inject_sensor_noise(state, std_dev=0.01):
        """Add Gaussian noise to state (sensor noise simulation)."""
        noise = np.random.normal(0, std_dev, size=state.shape)
        return state + noise

    @staticmethod
    def inject_latency(control_history, delay_steps=1):
        """Simulate actuator latency by delaying control application."""
        if len(control_history) <= delay_steps:
            return 0.0
        return control_history[-(delay_steps + 1)]