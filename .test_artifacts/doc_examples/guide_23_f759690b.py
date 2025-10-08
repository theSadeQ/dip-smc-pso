# Example from: docs\optimization_simulation\guide.md
# Index: 23
# Runnable: True
# Hash: f759690b

# MEMORY OPTIMIZATION: asarray creates view when input is already ndarray
x = np.asarray(initial_state, dtype=float)  # View if already float64 ndarray

# Unnecessary defensive copy eliminated
x_curr = x0  # No copy needed, immediately overwritten