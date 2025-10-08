# Example from: docs\factory_integration_documentation.md
# Index: 1
# Runnable: False
# Hash: 6991cb35

# example-metadata:
# runnable: false

def create_controller(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[list, np.ndarray]] = None
) -> Any:
    """
    Create a controller instance of the specified type.

    Thread-safe operation with comprehensive validation.

    Args:
        controller_type: Type of controller ('classical_smc', 'sta_smc', etc.)
        config: Configuration object (optional)
        gains: Controller gains array (optional)

    Returns:
        Configured controller instance

    Raises:
        ValueError: If controller_type is not recognized
        ImportError: If required dependencies are missing
    """