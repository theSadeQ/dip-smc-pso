# Example from: docs\factory_integration_documentation.md
# Index: 3
# Runnable: True
# Hash: 61136e5c

# Thread-safe factory operations
_factory_lock = threading.RLock()
_LOCK_TIMEOUT = 10.0  # seconds

def create_controller(controller_type: str, config: Optional[Any] = None,
                     gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """Thread-safe controller creation."""
    with _factory_lock:
        # Controller creation logic protected by lock
        return _create_controller_impl(controller_type, config, gains)