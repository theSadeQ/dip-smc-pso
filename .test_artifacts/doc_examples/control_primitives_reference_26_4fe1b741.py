# Example from: docs\controllers\control_primitives_reference.md
# Index: 26
# Runnable: False
# Hash: 4fe1b741

def safe_exp(
    x: NumericType,
    max_value: float = 700.0,
    warn: bool = False,
) -> NumericType:
    """Safe exponential with overflow protection.

    Mathematical Definition:
        safe_exp(x) = exp(min(x, max_value))

    Clips input to (-∞, max_value] to prevent overflow.
    Default max_value=700 is safe for IEEE 754 double precision.
    """