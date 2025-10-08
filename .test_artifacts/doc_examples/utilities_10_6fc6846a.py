# Example from: docs\guides\api\utilities.md
# Index: 10
# Runnable: True
# Hash: 6fc6846a

from src.utils.control import MovingAverageFilter

maf = MovingAverageFilter(window_size=10)

for control in control_sequence:
    smoothed = maf.update(control)