# Example from: docs\factory\configuration_reference.md
# Index: 1
# Runnable: False
# Hash: ad4a5b97

# example-metadata:
# runnable: false

# Thread-safe factory operations
_factory_lock = threading.RLock()

def create_controller(controller_type: str, config: Optional[Any] = None,
                     gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    with _factory_lock:
        # Thread-safe controller creation
        ...