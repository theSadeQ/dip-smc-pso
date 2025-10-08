# Example from: docs\memory_management_patterns.md
# Index: 3
# Runnable: False
# Hash: e497c739

class Controller:
    def cleanup(self):
        """Explicit memory cleanup (call before deletion)."""
        # Clear history buffers
        if hasattr(self, '_history') and isinstance(self._history, list):
            self._history.clear()

        # Nullify large arrays
        for attr in ['_state_buffer', '_control_buffer', '_surface_buffer']:
            if hasattr(self, attr):
                setattr(self, attr, None)

        # Clear dynamics reference
        if hasattr(self, '_dynamics_ref'):
            self._dynamics_ref = lambda: None