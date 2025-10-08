# Example from: docs\controllers\control_primitives_reference.md
# Index: 3
# Runnable: True
# Hash: a66cd125

def smooth_sign(
    x: Union[float, np.ndarray],
    epsilon: float = 0.01
) -> Union[float, np.ndarray]:
    """Smooth approximation of the sign function using tanh.

    Convenience wrapper for saturate() with tanh method.
    """