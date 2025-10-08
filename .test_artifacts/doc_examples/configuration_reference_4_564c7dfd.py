# Example from: docs\factory\configuration_reference.md
# Index: 4
# Runnable: False
# Hash: 564c7dfd

def _validate_controller_gains(
    gains: List[float],
    controller_info: Dict[str, Any]
) -> None:
    """Validate controller gains for stability and correctness."""

    # Length validation
    expected_count = controller_info['gain_count']
    if len(gains) != expected_count:
        raise ValueError(f"Controller requires {expected_count} gains, got {len(gains)}")

    # Numerical validation
    if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in gains):
        raise ValueError("All gains must be finite numbers")

    # Stability validation (SMC requirement)
    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive")