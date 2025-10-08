# Example from: docs\mathematical_foundations\smc_complete_theory.md
# Index: 1
# Runnable: True
# Hash: 8d095889

if np.linalg.cond(M) > 1e6:
    M_inv = np.linalg.pinv(M)  # Use pseudo-inverse
else:
    M_inv = np.linalg.inv(M)   # Direct inversion safe