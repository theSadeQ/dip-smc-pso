# Example from: docs\api\factory_system_api_reference.md
# Index: 1
# Runnable: False
# Hash: 7cc86cb0

# example-metadata:
# runnable: false

# Thread-safe factory operations with timeout protection
_factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds

def create_controller(controller_type, config=None, gains=None):
    with _factory_lock:
        # Thread-safe controller creation logic
        ...