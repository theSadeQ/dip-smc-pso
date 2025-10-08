# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 19
# Runnable: False
# Hash: 0f6bbb5c

# example-metadata:
# runnable: false

class ControlPrimitives:
    """Collection of control theory primitive functions.

    Provides reusable control primitives: saturation, dead zone, rate limiting,
    filtering, etc.

    Methods
    -------
    saturate(value, limit) -> float
        Saturate value to [-limit, +limit].
    dead_zone(value, threshold) -> float
        Apply dead zone (zero output if |value| < threshold).
    rate_limit(value, prev_value, max_rate, dt) -> float
        Limit rate of change.

    Examples
    --------
    >>> primitives = ControlPrimitives()
    >>> control = primitives.saturate(raw_control, max_force)
    """