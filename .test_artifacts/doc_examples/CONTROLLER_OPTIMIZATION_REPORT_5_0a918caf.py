# Example from: docs\reports\CONTROLLER_OPTIMIZATION_REPORT.md
# Index: 5
# Runnable: True
# Hash: 0a918caf

# Enhanced stability constraint validation
def validate_gains(self, gains_b: np.ndarray) -> np.ndarray:
    k1, k2 = gains_b[:, 0], gains_b[:, 1]
    valid = (k1 > 0.0) & (k2 > 0.0) & (k1 > k2)  # Strict K1 > K2
    return valid