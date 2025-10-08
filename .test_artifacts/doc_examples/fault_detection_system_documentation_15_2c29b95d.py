# Example from: docs\fault_detection_system_documentation.md
# Index: 15
# Runnable: False
# Hash: 2c29b95d

def test_weighted_residual_correction():
    """Verify weighted residual calculation is mathematically correct."""
    residual = np.array([0.1, 0.2, 0.3])
    weights = np.array([10.0, 1.0, 5.0])

    # Manual calculation
    weighted_residual = residual * weights  # [1.0, 0.2, 1.5]
    expected_norm = np.linalg.norm(weighted_residual)  # ≈ 1.844

    # FDI calculation
    fdi = FDIsystem(residual_states=[0, 1, 2], residual_weights=weights.tolist())
    # ... (call fdi.check with test data)

    assert abs(computed_norm - expected_norm) < 1e-10