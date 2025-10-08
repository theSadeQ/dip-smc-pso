# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 7
# Runnable: True
# Hash: 52a455e1

import numpy as np

# Estimate memory usage
def estimate_memory(batch_size, horizon, state_dim=6):
    """Estimate memory usage for batch simulation."""
    bytes_per_float = 8  # np.float64

    # States array: (batch_size, horizon+1, state_dim)
    states_size = batch_size * (horizon + 1) * state_dim * bytes_per_float

    # Controls array: (batch_size, horizon)
    controls_size = batch_size * horizon * bytes_per_float

    # Times array: (horizon+1,)
    times_size = (horizon + 1) * bytes_per_float

    total_bytes = states_size + controls_size + times_size
    total_mb = total_bytes / 1024 / 1024

    return total_mb

# Example
batch_sizes = [10, 100, 1000, 10000]
horizon = 1000  # 10 seconds @ dt=0.01

for bs in batch_sizes:
    mem = estimate_memory(bs, horizon)
    print(f"Batch size {bs:5d}: {mem:8.2f} MB")