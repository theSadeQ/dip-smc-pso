# Example from: docs\memory_management_patterns.md
# Index: 4
# Runnable: True
# Hash: 6ab887e1

class Controller:
    def __del__(self):
        """Automatic cleanup on deletion."""
        try:
            self.cleanup()
        except Exception:
            pass  # Never raise in destructor