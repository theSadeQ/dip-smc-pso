# Example from: docs\api\phase_4_2_completion_report.md
# Index: 12
# Runnable: False
# Hash: b63ee321

_factory_lock = threading.RLock()  # Reentrant allows nested calls
_LOCK_TIMEOUT = 10.0  # Prevents deadlocks

def create_controller(controller_type, config=None, gains=None):
    with _factory_lock:  # Automatic acquire/release
        # Thread-safe controller creation
        ...