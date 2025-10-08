# Example from: docs\fault_detection_system_documentation.md
# Index: 16
# Runnable: False
# Hash: 6507b499

# CORRECTED CUSUM update logic
if self.cusum_enabled:
    # Robust reference value selection
    if self.adaptive and mu is not None:
        ref = mu  # Use adaptive mean when available
    else:
        ref = self.residual_threshold  # Fallback to base threshold

    # Standard CUSUM update with negative clipping
    self._cusum = max(0.0, self._cusum + (residual_norm - ref))

    if self._cusum > self.cusum_threshold:
        self.tripped_at = t
        logging.info(f"CUSUM fault detected: {self._cusum:.4f} > {self.cusum_threshold}")
        return "FAULT", residual_norm