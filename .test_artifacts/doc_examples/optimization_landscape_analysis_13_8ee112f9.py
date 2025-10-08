# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 13
# Runnable: True
# Hash: 8ee112f9

from SALib.analyze import sobol

# Sample parameter space
from SALib.sample import saltelli
problem = {
    'num_vars': 6,
    'names': ['k1', 'k2', 'λ1', 'λ2', 'K', 'kd'],
    'bounds': [[0.1, 50], [0.1, 50], [0.1, 50],
               [0.1, 50], [1, 200], [0, 50]]
}

param_values = saltelli.sample(problem, 1000)  # 1000 samples

# Evaluate fitness
Y = np.array([evaluate_fitness(g) for g in param_values])

# Compute Sobol indices
Si = sobol.analyze(problem, Y)

print("First-order indices:", Si['S1'])
print("Total indices:", Si['ST'])