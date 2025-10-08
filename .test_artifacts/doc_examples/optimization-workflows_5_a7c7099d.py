# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 5
# Runnable: True
# Hash: a7c7099d

import matplotlib.pyplot as plt
import json

# Load PSO results (if history is saved)
with open('optimized_gains.json') as f:
    data = json.load(f)

if 'pso_history' in data:
    iterations = data['pso_history']['iterations']
    best_costs = data['pso_history']['best_costs']
    mean_costs = data['pso_history']['mean_costs']

    # Plot convergence
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(iterations, best_costs, 'b-', linewidth=2, label='Global Best')
    ax.plot(iterations, mean_costs, 'r--', linewidth=1, label='Swarm Mean')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Cost')
    ax.set_title('PSO Convergence')
    ax.legend()
    ax.grid(True)
    ax.set_yscale('log')  # Log scale for better visibility
    plt.show()