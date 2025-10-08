# Example from: docs\test_infrastructure_validation_report.md
# Index: 2
# Runnable: True
# Hash: e316acae

@pytest.mark.convergence
@pytest.mark.numerical_stability
def test_sliding_surface_reachability():
    """Validate finite-time convergence to sliding surface."""
    # Mathematical property: |s(t)| → 0 in finite time
    # Lyapunov candidate: V = 0.5 * s²
    # Reachability condition: s * ṡ ≤ -η|s| for η > 0