# Example from: docs\architecture\controller_system_architecture.md
# Index: 15
# Runnable: False
# Hash: 68d10e27

class MemoryEfficientController:
    """Memory-efficient controller with bounded collections."""

    def __init__(self, max_history_size: int = 10000):
        self.max_history_size = max_history_size
        self._history_buffer = collections.deque(maxlen=max_history_size)

    def update_history(self, control_data: Dict[str, Any]) -> None:
        """Update history with automatic memory management."""

        # Add new data point
        self._history_buffer.append(control_data)

        # Automatic cleanup if buffer full
        if len(self._history_buffer) >= self.max_history_size:
            # Optionally compress older data
            self._compress_old_history()

    def _compress_old_history(self) -> None:
        """Compress older history data to save memory."""

        # Keep recent data at full resolution
        recent_data = list(self._history_buffer)[-1000:]

        # Subsample older data
        old_data = list(self._history_buffer)[:-1000]
        subsampled_old = old_data[::10]  # Keep every 10th point

        # Rebuild buffer
        self._history_buffer.clear()
        self._history_buffer.extend(subsampled_old + recent_data)