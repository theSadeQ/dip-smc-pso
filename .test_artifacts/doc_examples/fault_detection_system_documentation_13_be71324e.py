# Example from: docs\fault_detection_system_documentation.md
# Index: 13
# Runnable: True
# Hash: be71324e

# WRONG: Weight applied after norm computation
residual_norm = np.linalg.norm(residual[self.residual_states])
if weights is not None:
    residual_norm *= np.linalg.norm(weights)  # INCORRECT