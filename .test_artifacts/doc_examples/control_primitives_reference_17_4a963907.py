# Example from: docs\controllers\control_primitives_reference.md
# Index: 17
# Runnable: False
# Hash: 4a963907

def require_finite(
    value: Union[float, int, None],
    name: str
) -> float:
    """Validate that a value is finite.

    Args:
        value: The numeric quantity to validate
        name: Parameter name

    Returns:
        Validated value cast to float

    Raises:
        ValueError: If value is None, infinity, or NaN
    """