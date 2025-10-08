# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 17
# Runnable: False
# Hash: 44a4088b

# Thread-safe factory operations
_factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds

def create_controller(...):
    """Thread-safe controller creation."""
    with _factory_lock:
        # Factory logic with timeout protection
        pass