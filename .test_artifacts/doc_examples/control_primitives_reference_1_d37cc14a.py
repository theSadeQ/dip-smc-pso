# Example from: docs\controllers\control_primitives_reference.md
# Index: 1
# Runnable: False
# Hash: d37cc14a

def saturate(
    sigma: Union[float, np.ndarray],
    epsilon: float,
    method: Literal["tanh", "linear"] = "tanh",
    slope: float = 3.0
) -> Union[float, np.ndarray]:
    """Continuous approximation of sign(sigma) within a boundary layer.

    Args:
        sigma: Sliding surface value(s)
        epsilon: Boundary-layer half-width (must be > 0)
        method: "tanh" (default) or "linear"
        slope: Slope parameter for tanh switching (default: 3.0)

    Returns:
        Continuous switching signal
    """