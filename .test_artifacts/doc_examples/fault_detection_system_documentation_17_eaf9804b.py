# Example from: docs\fault_detection_system_documentation.md
# Index: 17
# Runnable: False
# Hash: eaf9804b

# example-metadata:
# runnable: false

def check(self, t, meas, u, dt, dynamics_model):
    # ... validation and prediction logic ...

    # FIXED: Always record history, including first measurement
    self.times.append(t)
    self.residuals.append(residual_norm)

    # Ensure history consistency
    assert len(self.times) == len(self.residuals), "History synchronization error"

    # ... rest of detection logic ...