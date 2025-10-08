# Example from: docs\issue_12_chattering_reduction_resolution.md
# Index: 4
# Runnable: True
# Hash: 0b61835b

def sign_switching(s, epsilon=0.0):
    """DEPRECATED - causes severe chattering.

    WARNING: Use tanh_switching(s, epsilon, slope=3.0) instead.
    """
    warnings.warn("sign_switching() causes severe chattering", DeprecationWarning)
    return np.sign(s)