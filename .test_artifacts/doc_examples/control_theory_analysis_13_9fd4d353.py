# Example from: docs\testing\reports\2025-09-30\technical\control_theory_analysis.md
# Index: 13
# Runnable: False
# Hash: 9fd4d353

# Implementation Priority: HIGH
class AdaptiveFaultDetection:
    def __init__(self, base_threshold=0.135, decay_rate=20.0):
        self.base_threshold = base_threshold
        self.decay_rate = decay_rate
        self.initial_threshold_offset = 0.05

    def compute_adaptive_threshold(self, time):
        transient_compensation = self.initial_threshold_offset * np.exp(-self.decay_rate * time)
        return self.base_threshold + transient_compensation

    def detect_fault(self, residual, time):
        threshold = self.compute_adaptive_threshold(time)
        return residual > threshold