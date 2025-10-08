# Example from: docs\guides\api\utilities.md
# Index: 7
# Runnable: True
# Hash: bc1910dd

from src.utils.control import apply_deadzone

control = 2.5
deadzone_threshold = 5.0

# Linear deadzone
output = apply_deadzone(control, deadzone_threshold)
# Returns: 0.0 (below threshold)

control = 7.5
output = apply_deadzone(control, deadzone_threshold)
# Returns: 2.5 (7.5 - 5.0)

# Smooth deadzone
from src.utils.control import smooth_deadzone

output = smooth_deadzone(control, deadzone_threshold, smoothness=0.5)