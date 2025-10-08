# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 12
# Runnable: True
# Hash: f330f694

def cleanup(self):
    """Explicit cleanup for long-running processes."""
    self._dynamics_ref = None
    logger.debug(f"{self.__class__.__name__} cleaned up")

def __del__(self):
    """Automatic cleanup on garbage collection."""
    self.cleanup()