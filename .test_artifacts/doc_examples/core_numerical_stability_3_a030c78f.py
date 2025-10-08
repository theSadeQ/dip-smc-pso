# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 3
# Runnable: True
# Hash: a030c78f

from src.plant.core import NumericalInstabilityError, MatrixInverter

inverter = MatrixInverter()
try:
    M_inv = inverter.invert_matrix(M)
except NumericalInstabilityError as e:
    print(f"Matrix inversion failed: {e}")
    # Handle error (use approximation, skip timestep, etc.)