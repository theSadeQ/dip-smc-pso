# Example from: docs\reference\plant\models_base_dynamics_interface.md
# Index: 8
# Runnable: True
# Hash: 0de60fb3

import time
from numba import njit

# Enable Numba JIT compilation for hot loops
@njit
def batch_dynamics_step(states, controls, params):
    """Vectorized dynamics computation."""
    N = states.shape[0]
    state_dots = np.zeros_like(states)
    for i in range(N):
        state_dots[i] = dynamics_core_numba(states[i], controls[i], params)
    return state_dots

# Benchmark
N = 1000
states = np.random.randn(N, 6)
controls = np.random.randn(N, 1)

start = time.perf_counter()
results = batch_dynamics_step(states, controls, params)
elapsed = time.perf_counter() - start

print(f"Processed {N} states in {elapsed*1000:.2f}ms")
print(f"Throughput: {N/elapsed:.0f} states/sec")