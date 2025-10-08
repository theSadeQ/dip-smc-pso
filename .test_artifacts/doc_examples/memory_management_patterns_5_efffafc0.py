# Example from: docs\memory_management_patterns.md
# Index: 5
# Runnable: False
# Hash: efffafc0

class Controller:
    def reset(self):
        """Reset controller state with memory cleanup."""
        # Original reset logic
        self._integral_state = 0.0
        self._previous_error = 0.0

        # NEW: Clear history buffers
        if hasattr(self, '_history'):
            self._history.clear()

        # NEW: Reset large arrays
        self._state_buffer = None
        self._control_buffer = None