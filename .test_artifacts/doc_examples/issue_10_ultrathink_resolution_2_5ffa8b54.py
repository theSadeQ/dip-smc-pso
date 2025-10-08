# Example from: docs\reports\issue_10_ultrathink_resolution.md
# Index: 2
# Runnable: True
# Hash: 5ffa8b54

# Import actual implementation (line 563)
from src.plant.core.numerical_stability import MatrixInverter, AdaptiveRegularizer

# Initialize with production parameters (lines 566-572)
regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-4,
    max_condition_number=1e14,
    min_regularization=1e-10,
    use_fixed_regularization=False
)
matrix_inverter = MatrixInverter(regularizer=regularizer)

# Test actual implementation, not mock (lines 575-647)
# - Test 3 matrices (cond numbers: 1e12, 1e5, 1e12)
# - Validate zero LinAlgError exceptions
# - Adaptive tolerance based on conditioning