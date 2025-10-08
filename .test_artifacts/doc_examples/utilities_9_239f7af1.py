# Example from: docs\guides\api\utilities.md
# Index: 9
# Runnable: True
# Hash: 239f7af1

from src.utils.control import LowPassFilter

# Create filter
lpf = LowPassFilter(cutoff_freq=10.0, dt=0.01)

# Filter control signal
controls = []
for i in range(len(control_sequence)):
    filtered = lpf.update(control_sequence[i])
    controls.append(filtered)

# Reset filter
lpf.reset()