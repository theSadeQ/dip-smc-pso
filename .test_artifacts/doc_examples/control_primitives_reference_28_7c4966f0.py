# Example from: docs\controllers\control_primitives_reference.md
# Index: 28
# Runnable: False
# Hash: 7c4966f0

def safe_normalize(
    vector: np.ndarray,
    ord: Optional[Union[int, float, str]] = 2,
    axis: Optional[int] = None,
    min_norm: float = 1e-15,
    fallback: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Safe vector normalization with zero-norm protection.

    Mathematical Definition:
        safe_normalize(v) = v / max(||v||, min_norm)
    """