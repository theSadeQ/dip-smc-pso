# Example from: docs\reference\simulation\engines_vector_sim.md
# Index: 2
# Runnable: True
# Hash: 3403b312

# Good: C-contiguous
X = np.ascontiguousarray(X)  # Row-major

# Bad: Non-contiguous views
X_bad = X[:, ::2]  # Strided access