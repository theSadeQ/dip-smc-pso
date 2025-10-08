# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 16
# Runnable: False
# Hash: 731f5c8b

# example-metadata:
# runnable: false

def _validate_controller_gains(
    gains: List[float],
    controller_info: Dict[str, Any],
    controller_type: str
) -> None:
    """
    Validate controller gains with mathematical constraints.

    Raises:
        ValueError: If gains violate stability or physical constraints
    """