# Example from: docs\testing\reports\2025-09-30\technical\resolution_roadmap.md
# Index: 2
# Runnable: False
# Hash: 8ba7c428

# example-metadata:
# runnable: false

# File: src/utils/monitoring/fault_detection.py
class AdaptiveFaultDetection:
    """Enhanced FDI with time-varying thresholds and statistical validation."""

    def __init__(self, config: FDIConfig):
        self.base_threshold = 0.135          # Calibrated base threshold
        self.transient_offset = 0.05         # Initial transient allowance
        self.decay_rate = 20.0               # Exponential decay rate
        self.statistical_window = 10         # Rolling window for statistics
        self.confidence_level = 0.95         # Statistical confidence

    def compute_adaptive_threshold(self, time: float) -> float:
        """Time-varying threshold to handle initial transients."""
        transient_compensation = self.transient_offset * np.exp(-self.decay_rate * time)
        return self.base_threshold + transient_compensation

    def detect_fault_with_statistics(self, residual: float, time: float) -> FaultStatus:
        """Statistical fault detection with false positive reduction."""
        threshold = self.compute_adaptive_threshold(time)

        # Basic threshold check
        exceeds_threshold = residual > threshold

        # Statistical validation
        if exceeds_threshold:
            return self._validate_fault_statistically(residual, threshold)

        return FaultStatus(detected=False, confidence=0.0, type=None)