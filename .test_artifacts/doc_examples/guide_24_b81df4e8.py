# Example from: docs\optimization_simulation\guide.md
# Index: 24
# Runnable: True
# Hash: b81df4e8

# MEMORY OPTIMIZATION: broadcast_to returns view
init_b = np.broadcast_to(init, (B, init.shape[0]))

# Only copy when writeable buffer needed
init_b = init_b.copy()