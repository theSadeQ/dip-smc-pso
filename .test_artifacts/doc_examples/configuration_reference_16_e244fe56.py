# Example from: docs\factory\configuration_reference.md
# Index: 16
# Runnable: True
# Hash: e244fe56

def create_controller(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[list, np.ndarray]] = None
) -> Any:
    """
    Create a controller instance with comprehensive validation and error handling.

    Thread-safe and supports multiple calling patterns for flexibility.
    """