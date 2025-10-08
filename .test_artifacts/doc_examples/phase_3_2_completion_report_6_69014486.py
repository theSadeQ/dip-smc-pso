# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 6
# Runnable: True
# Hash: 69014486

from src.controllers.adaptive_smc import AdaptiveSMC

# Conservative adaptation rate recommended
controller = AdaptiveSMC(
    gains=[25.0, 18.0, 15.0, 10.0, 4.0],
    adaptation_rate=4.0,  # Lower values for slower adaptation
    max_force=100.0
)

# Log adapted gains for diagnostics
if iteration % 100 == 0:
    log_info(f"Adapted gains: {controller.get_current_gains()}")