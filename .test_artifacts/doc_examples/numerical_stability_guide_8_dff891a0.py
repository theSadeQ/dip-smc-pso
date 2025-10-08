# Example from: docs\numerical_stability_guide.md
# Index: 8
# Runnable: True
# Hash: dff891a0

from src.plant.core.numerical_stability import AdaptiveRegularizer, MatrixInverter

# Initialize with standardized parameters
regularizer = AdaptiveRegularizer(
    regularization_alpha=1e-4,        # Base scaling factor
    max_condition_number=1e14,        # Condition threshold
    min_regularization=1e-10,         # Safety floor
    use_fixed_regularization=False    # Enable adaptive mode
)

matrix_inverter = MatrixInverter(regularizer=regularizer)

# Robust matrix inversion
try:
    M_inv = matrix_inverter.invert_matrix(M)
except NumericalInstabilityError as e:
    print(f"Matrix inversion failed: {e}")