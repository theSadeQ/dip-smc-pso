# Example from: docs\fdi_threshold_calibration_methodology.md
# Index: 5
# Runnable: True
# Hash: 3ee880db

from src.analysis.fault_detection.fdi import FDIsystem

fdi = FDIsystem(
    residual_threshold=0.145,  # Post-Kalman filtering
    use_ekf=True,              # Enable Kalman-based residual
    ekf_process_noise=0.01,
    ekf_measurement_noise=0.05
)