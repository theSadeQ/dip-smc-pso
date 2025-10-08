# Example from: docs\benchmarks\phase_3_2_completion_report.md
# Index: 5
# Runnable: True
# Hash: 8dd80f5d

from src.controllers.sta_smc import STASMC

# Ensure K1 > K2 for discontinuous gain dominance
controller = STASMC(
    gains=[25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
    max_force=100.0
)

# Validate constraint (should be done automatically by factory)
assert controller.gains[0] > controller.gains[1], "K1 must be > K2"