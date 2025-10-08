# Example from: docs\reports\issue_10_ultrathink_resolution.md
# Index: 1
# Runnable: True
# Hash: b306d8e3

# Import robust infrastructure (line 24)
from src.plant.core.numerical_stability import MatrixInverter, AdaptiveRegularizer

# Initialize in constructor (lines 55-61)
self.adaptive_regularizer = AdaptiveRegularizer(
    regularization_alpha=regularization,
    max_condition_number=1e14,
    min_regularization=regularization,
    use_fixed_regularization=False
)
self.matrix_inverter = MatrixInverter(regularizer=self.adaptive_regularizer)

# Replace direct inversion (lines 81-82)
# OLD: M_reg = self._regularize_matrix(M); M_inv = np.linalg.inv(M_reg)
# NEW:
M_inv = self.matrix_inverter.invert_matrix(M)

# Update controllability check (line 216)
M_inv = self.matrix_inverter.invert_matrix(M)