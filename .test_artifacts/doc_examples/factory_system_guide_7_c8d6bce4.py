# Example from: docs\controllers\factory_system_guide.md
# Index: 7
# Runnable: False
# Hash: c8d6bce4

# Thread-safe factory operations with timeout protection
_factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds

def create_controller(controller_type: str, ...) -> Any:
    with _factory_lock:
        # Thread-safe controller creation
        controller_info = _get_controller_info(controller_type)
        # ... validation and instantiation