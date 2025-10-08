# Example from: docs\api\optimization_module_api_reference.md
# Index: 6
# Runnable: True
# Hash: ed59e0ef

# Run optimization with default settings
result = tuner.optimise()

# Extract optimized gains
optimized_gains = result['best_pos']
final_cost = result['best_cost']
convergence_history = result['cost_history']

# Plot convergence
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(convergence_history)
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.title('PSO Convergence History')
plt.yscale('log')
plt.grid(True)
plt.savefig('pso_convergence.png')