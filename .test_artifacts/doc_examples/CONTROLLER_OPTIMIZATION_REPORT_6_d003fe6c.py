# Example from: docs\reports\CONTROLLER_OPTIMIZATION_REPORT.md
# Index: 6
# Runnable: True
# Hash: d003fe6c

@contextmanager
def acquire_minimal_lock(self, resource_id: str, timeout: float = 5.0):
    """Acquire lock with minimal hold time and performance tracking."""
    # Lock acquisition with contention monitoring
    # Automatic hold time statistics
    # Deadlock prevention with timeout