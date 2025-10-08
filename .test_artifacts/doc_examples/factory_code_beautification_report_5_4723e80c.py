# Example from: docs\reports\factory_code_beautification_report.md
# Index: 5
# Runnable: False
# Hash: 4723e80c

# example-metadata:
# runnable: false

# Thread-safe factory operations with timeout protection
_factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds

def create_controller(...) -> ControllerProtocol:
    with _factory_lock:
        # Thread-safe controller creation