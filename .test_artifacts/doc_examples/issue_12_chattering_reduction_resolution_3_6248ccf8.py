# Example from: docs\issue_12_chattering_reduction_resolution.md
# Index: 3
# Runnable: False
# Hash: 6248ccf8

# example-metadata:
# runnable: false

def _tanh_switching(self, s, epsilon, slope=3.0):
    """Configurable slope for tunable smoothness.

    Formula: tanh((slope * s) / ε)

    Slope Parameter:
    - Original: Implicit 10+ (steep, near-discontinuous)
    - Optimized: 3.0 (gentle, smooth transitions)
    - Range: 2-5 for chattering reduction
    """
    ratio = (slope * s) / epsilon
    if abs(ratio) > 700:
        return np.sign(s)
    return np.tanh(ratio)