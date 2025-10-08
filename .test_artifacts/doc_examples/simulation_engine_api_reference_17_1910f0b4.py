# Example from: docs\api\simulation_engine_api_reference.md
# Index: 17
# Runnable: True
# Hash: 1910f0b4

# MEMORY OPTIMIZATION: asarray creates view when input is already ndarray
x0 = np.asarray(initial_state, dtype=float).reshape(-1)  # View, not copy
x_curr = x0  # View, immediately overwritten at line 323
x_next = np.asarray(x_next, dtype=float).reshape(-1)  # View when possible