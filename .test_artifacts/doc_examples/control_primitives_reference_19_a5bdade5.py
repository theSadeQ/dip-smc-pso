# Example from: docs\controllers\control_primitives_reference.md
# Index: 19
# Runnable: False
# Hash: a5bdade5

# example-metadata:
# runnable: false

def safe_divide(
    numerator: NumericType,
    denominator: NumericType,
    epsilon: float = 1e-12,
    fallback: float = 0.0,
    warn: bool = False,
) -> NumericType:
    """Safe division with epsilon threshold protection against zero division.

    Mathematical Definition:
        safe_divide(a, b) = a / max(|b|, ε) * sign(b)

    Args:
        numerator: Dividend (scalar or array)
        denominator: Divisor (scalar or array)
        epsilon: Minimum safe denominator magnitude (default: 1e-12)
        fallback: Value to return if denominator is exactly zero (default: 0.0)
        warn: Issue warning when epsilon protection triggers (default: False)
    """