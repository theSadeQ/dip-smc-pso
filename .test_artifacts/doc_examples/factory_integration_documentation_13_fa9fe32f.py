# Example from: docs\factory_integration_documentation.md
# Index: 13
# Runnable: False
# Hash: fa9fe32f

def _validate_controller_gains(
    gains: List[float],
    controller_info: Dict[str, Any]
) -> None:
    """Validate controller gains with domain-specific checks."""

    # Basic structural validation
    expected_count = controller_info['gain_count']
    if len(gains) != expected_count:
        raise ValueError(f"Expected {expected_count} gains, got {len(gains)}")

    # Numerical validation
    if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in gains):
        raise ValueError("All gains must be finite numbers")

    # Domain-specific validation
    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive for SMC stability")