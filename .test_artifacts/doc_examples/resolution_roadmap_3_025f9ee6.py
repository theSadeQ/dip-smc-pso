# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 3
# Runnable: False
# Hash: 025f9ee6

# Test file: tests/test_monitoring/test_adaptive_fault_detection.py
def test_transient_handling():
    """Verify FDI handles initial transients correctly."""
    fdi = AdaptiveFaultDetection(FDIConfig())

    # Test early time period (t < 0.1s)
    early_threshold = fdi.compute_adaptive_threshold(0.05)
    assert early_threshold > 0.15  # Allow for transients

    # Test steady-state period (t > 1.0s)
    steady_threshold = fdi.compute_adaptive_threshold(1.0)
    assert abs(steady_threshold - 0.135) < 1e-3

def test_false_positive_reduction():
    """Verify statistical validation reduces false positives."""
    fdi = AdaptiveFaultDetection(FDIConfig())

    # Simulate normal operation with noise
    residuals = [0.132, 0.128, 0.135, 0.130, 0.133]  # Normal variation
    faults = [fdi.detect_fault_with_statistics(r, 0.1) for r in residuals]

    false_positive_rate = sum(f.detected for f in faults) / len(faults)
    assert false_positive_rate < 0.05  # < 5% false positive rate