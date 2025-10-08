# Example from: docs\controllers\control_primitives_reference.md
# Index: 21
# Runnable: True
# Hash: f3bf276f

def safe_reciprocal(
    x: NumericType,
    epsilon: float = 1e-12,
    fallback: float = 0.0,
    warn: bool = False,
) -> NumericType:
    """Safe reciprocal (1/x) with epsilon protection.

    Convenience wrapper for safe_divide(1.0, x).
    """