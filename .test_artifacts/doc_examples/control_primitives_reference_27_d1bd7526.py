# Example from: docs\controllers\control_primitives_reference.md
# Index: 27
# Runnable: False
# Hash: d1bd7526

def safe_norm(
    vector: np.ndarray,
    ord: Optional[Union[int, float, str]] = 2,
    axis: Optional[int] = None,
    min_norm: float = 1e-15,
) -> Union[float, np.ndarray]:
    """Safe vector/matrix norm with zero-norm protection.

    Mathematical Definition:
        safe_norm(v) = max(||v||_p, min_norm)
    """