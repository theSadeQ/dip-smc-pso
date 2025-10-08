# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 4
# Runnable: True
# Hash: 063b2d9f

import json
import matplotlib.pyplot as plt
import numpy as np

# Load PSO log (if saved during optimization)
pso_data = json.load(open('optimized_classical_gains.json'))

# Extract cost history
if 'pso_history' in pso_data:
    iterations = pso_data['pso_history']['iterations']
    best_costs = pso_data['pso_history']['best_costs']
    mean_costs = pso_data['pso_history']['mean_costs']

    plt.figure(figsize=(10, 6))
    plt.plot(iterations, best_costs, 'b-', linewidth=2, label='Global Best')
    plt.plot(iterations, mean_costs, 'r--', linewidth=1, label='Swarm Mean')
    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('PSO Convergence: Classical SMC')
    plt.legend()
    plt.grid(True)
    plt.semilogy()  # Log scale for better visibility
    plt.show()