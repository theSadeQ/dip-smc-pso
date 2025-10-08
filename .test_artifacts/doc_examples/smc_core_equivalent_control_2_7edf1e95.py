# Example from: docs\reference\controllers\smc_core_equivalent_control.md
# Index: 2
# Runnable: True
# Hash: 7edf1e95

# Check matrix conditioning before inversion
M = dynamics.compute_mass_matrix(state)
cond_number = np.linalg.cond(M)

print(f"Condition number of M: {cond_number:.2e}")

if cond_number > 1e6:
    print("Warning: Ill-conditioned matrix, increasing regularization")
    eq_control.set_regularization(alpha=1e-4)
else:
    print("Matrix well-conditioned")