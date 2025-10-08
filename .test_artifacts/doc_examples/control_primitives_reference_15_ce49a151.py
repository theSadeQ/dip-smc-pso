# Example from: docs\controllers\control_primitives_reference.md
# Index: 15
# Runnable: False
# Hash: ce49a151

def require_positive(
    value: Union[float, int, None],
    name: str,
    *,
    allow_zero: bool = False
) -> float:
    """Validate that a numeric value is positive (or non-negative).

    Args:
        value: The numeric quantity to validate
        name: Parameter name (used in error message)
        allow_zero: When True, value of exactly zero is allowed

    Returns:
        Validated value cast to float

    Raises:
        ValueError: If value is None, not finite, or not positive
    """