# Example from: docs\guides\api\utilities.md
# Index: 8
# Runnable: True
# Hash: ff133966

from src.utils.control import smooth_sign

s = 0.5  # Sliding surface value
epsilon = 0.01  # Boundary layer

# Standard sign (discontinuous)
sign_output = np.sign(s)  # Returns: 1.0

# Smooth sign (continuous)
smooth_output = smooth_sign(s, epsilon)
# Returns: tanh(s/epsilon)

# Linear approximation in boundary layer
from src.utils.control import linear_sign

linear_output = linear_sign(s, epsilon)
# Returns: s/epsilon if |s| < epsilon, else sign(s)