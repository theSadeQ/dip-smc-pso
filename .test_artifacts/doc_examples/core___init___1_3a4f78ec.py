# Example from: docs\reference\plant\core___init__.md
# Index: 1
# Runnable: True
# Hash: 3a4f78ec

# Clean separation
M = compute_mass_matrix(q, params)        # Physics
M_inv = robust_inverse(M)                 # Numerical
is_valid = validate_state(x)              # Validation