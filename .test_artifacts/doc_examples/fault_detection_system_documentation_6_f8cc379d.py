# Example from: docs\fault_detection_system_documentation.md
# Index: 6
# Runnable: False
# Hash: f8cc379d

@given(residuals=arrays(float, min_size=10, max_size=1000))
@assume(all(r >= 0 for r in residuals))
def test_adaptive_threshold_monotonicity(residuals):
    """Adaptive threshold should increase with residual variance."""
    fdi = FDIsystem(adaptive=True)

    # Feed residuals to build window
    for r in residuals:
        fdi._residual_window.append(r)

    # Higher variance should result in higher threshold
    if len(residuals) >= fdi.window_size:
        threshold = compute_adaptive_threshold(fdi._residual_window)
        assert threshold >= fdi.residual_threshold