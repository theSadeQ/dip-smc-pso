# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 4
# Runnable: True
# Hash: f1485d06

from src.controllers.classic_smc import ClassicalSMC

# Optimized gains (from PSO validation)
controller = ClassicalSMC(
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=100.0,
    boundary_layer=0.01  # Tune to balance tracking vs chattering
)

# Monitor control saturation
control, _ = controller.compute_control(state)
if abs(control) >= 99.0:
    log_warning("Control approaching saturation limit")