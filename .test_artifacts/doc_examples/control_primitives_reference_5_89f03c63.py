# Example from: docs\controllers\control_primitives_reference.md
# Index: 5
# Runnable: False
# Hash: 89f03c63

def dead_zone(
    x: Union[float, np.ndarray],
    threshold: float
) -> Union[float, np.ndarray]:
    """Apply dead zone to input signal.

    Args:
        x: Input signal
        threshold: Dead zone threshold (must be positive)

    Returns:
        Signal with dead zone applied
    """