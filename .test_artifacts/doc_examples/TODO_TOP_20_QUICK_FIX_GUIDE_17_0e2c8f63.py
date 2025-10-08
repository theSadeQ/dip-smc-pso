# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 17
# Runnable: False
# Hash: 0e2c8f63

# example-metadata:
# runnable: false

class DefaultPhysicsConfig:
    """Default physics parameters for double-inverted pendulum.

    Provides standard physical parameters based on Quanser hardware specifications.

    Attributes
    ----------
    m1, m2 : float
        Masses of first and second pendulum (kg).
    L1, L2 : float
        Lengths of pendulum links (m).
    g : float
        Gravitational acceleration (m/s²).
    friction : float
        Cart friction coefficient.

    Examples
    --------
    >>> config = DefaultPhysicsConfig()
    >>> dynamics = SimplifiedDynamicsModel(config)
    """