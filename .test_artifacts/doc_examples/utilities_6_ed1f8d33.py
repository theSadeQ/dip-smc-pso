# Example from: docs\guides\api\utilities.md
# Index: 6
# Runnable: True
# Hash: ed1f8d33

from src.utils.control import saturate

control = 150.0
max_force = 100.0

# Hard saturation
saturated = saturate(control, max_force)
# Returns: 100.0

# Symmetric saturation
saturated = saturate(control, -max_force, max_force)

# Soft saturation (smooth)
from src.utils.control import soft_saturate

soft_sat = soft_saturate(control, max_force, smoothness=0.1)
# Smooth transition near limits