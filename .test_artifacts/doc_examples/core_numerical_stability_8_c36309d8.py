# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 8
# Runnable: True
# Hash: c36309d8

try:
    M_inv = inverter.invert_matrix(M)
    q_ddot = M_inv @ forcing
except NumericalInstabilityError:
    print("Matrix inversion failed - using approximate dynamics")
    q_ddot = np.zeros(3)  # Safe fallback