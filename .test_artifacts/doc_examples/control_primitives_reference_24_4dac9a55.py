# Example from: docs\controllers\control_primitives_reference.md
# Index: 24
# Runnable: True
# Hash: 4dac9a55

def safe_log(
    x: NumericType,
    min_value: float = 1e-15,
    warn: bool = False,
) -> NumericType:
    """Safe natural logarithm with zero/negative protection.

    Mathematical Definition:
        safe_log(x) = ln(max(x, min_value))
    """