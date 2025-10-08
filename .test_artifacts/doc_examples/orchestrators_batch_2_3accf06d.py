# Example from: docs\reference\simulation\orchestrators_batch.md
# Index: 2
# Runnable: True
# Hash: 3accf06d

@njit(parallel=True, fastmath=True)
def batch_simulate(x0_batch, u_batch, dt, steps):
    # Compiled to optimized machine code