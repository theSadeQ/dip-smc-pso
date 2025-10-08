# Example from: docs\fdi_threshold_calibration_methodology.md
# Index: 4
# Runnable: False
# Hash: 90795d5e

# example-metadata:
# runnable: false

def test_fixed_threshold_operation():
    """Verify FDI operates with fixed threshold."""
    fdi = FDIsystem(
        residual_threshold=0.150,  # Updated from 0.100
        persistence_counter=10
    )

    # Test normal operation (no fault)
    for t in np.linspace(0, 1.0, 100):
        measurement = np.zeros(6) + np.random.normal(0, 0.05, 6)
        status, residual = fdi.check(t, measurement, 0.0, 0.01, dynamics)

        if residual < 0.150:
            assert status == "OK"