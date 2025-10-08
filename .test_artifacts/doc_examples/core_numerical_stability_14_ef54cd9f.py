# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 14
# Runnable: True
# Hash: ef54cd9f

from src.plant.core import MatrixInverter, NumericalInstabilityError

inverter = MatrixInverter()

try:
    M_inv = inverter.invert_matrix(M)
    print("Inversion successful")
except NumericalInstabilityError as e:
    print(f"Inversion failed: {e}")