# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 11
# Runnable: False
# Hash: 9228c67b

# Coarse sweep first
k1_coarse = np.linspace(5, 30, 5)
k2_coarse = np.linspace(5, 30, 5)

# Run coarse sweep...
# Identify best region

# Refine around best point
k1_best, k2_best = 15.0, 20.0  # Example
k1_fine = np.linspace(k1_best-5, k1_best+5, 20)
k2_fine = np.linspace(k2_best-5, k2_best+5, 20)

# Run fine sweep in refined region...