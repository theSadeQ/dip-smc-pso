# Example from: docs\testing\guides\performance_benchmarking.md
# Index: 7
# Runnable: True
# Hash: b6cd0377

def compute_cost(states):
    costs = []
    for state in states:
        cost = sum(state**2)  # Slow Python loop
        costs.append(cost)
    return np.array(costs)