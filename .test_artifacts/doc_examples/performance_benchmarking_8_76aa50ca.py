# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 8
# Runnable: True
# Hash: 76aa50ca

def compute_cost(states):
    return np.sum(states**2, axis=1)  # Vectorized NumPy