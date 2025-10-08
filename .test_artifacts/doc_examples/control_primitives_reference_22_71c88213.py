# Example from: docs\controllers\control_primitives_reference.md
# Index: 22
# Runnable: False
# Hash: 71c88213

# example-metadata:
# runnable: false

def safe_sqrt(
    x: NumericType,
    min_value: float = 1e-15,
    warn: bool = False,
) -> NumericType:
    """Safe square root with negative value protection.

    Mathematical Definition:
        safe_sqrt(x) = √(max(x, min_value))

    Clips input to [min_value, ∞) before applying sqrt to prevent
    domain errors from numerical noise producing negative values.
    """