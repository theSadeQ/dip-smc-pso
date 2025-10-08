# Example from: docs\guides\api\configuration.md
# Index: 14
# Runnable: False
# Hash: 529974fd

# example-metadata:
# runnable: false

def validate_physics_params(params: DIPParams):
    """Validate physical constraints."""
    # Positive masses
    if params.m0 <= 0 or params.m1 <= 0 or params.m2 <= 0:
        raise ValueError("Masses must be positive")

    # Positive lengths
    if params.l1 <= 0 or params.l2 <= 0:
        raise ValueError("Lengths must be positive")

    # Reasonable gravity
    if not (9.0 <= params.g <= 10.0):
        raise ValueError("Gravity should be ~9.81 m/s²")

    # Friction coefficients non-negative
    if params.b0 < 0 or params.b1 < 0 or params.b2 < 0:
        raise ValueError("Friction coefficients must be non-negative")

    return True