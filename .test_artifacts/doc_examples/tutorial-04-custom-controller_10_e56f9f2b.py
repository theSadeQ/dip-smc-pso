# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 10
# Runnable: True
# Hash: e56f9f2b

try:
    M_inv = np.linalg.inv(M)
except np.linalg.LinAlgError:
    logger.warning("Singular matrix, using robust control only")
    return 0.0  # Fallback