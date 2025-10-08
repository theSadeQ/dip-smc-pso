# Example from: docs\fdi_threshold_calibration_methodology.md
# Index: 3
# Runnable: False
# Hash: 27c76192

# example-metadata:
# runnable: false

def check(self, t, meas, u, dt, dynamics_model):
    # ... residual computation ...

    if self.hysteresis_enabled:
        # Use upper threshold for fault detection
        threshold = self.hysteresis_upper
    else:
        # Legacy single-threshold behavior
        threshold = self.residual_threshold

    # Persistence filtering
    if residual_norm > threshold:
        self._counter += 1
        if self._counter >= self.persistence_counter:
            self.tripped_at = t
            return "FAULT", residual_norm
    else:
        self._counter = 0  # Reset on good measurement

    return "OK", residual_norm