# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 7
# Runnable: True
# Hash: ee343e83

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def compare_optimization_results(result_files):
    """Compare PSO optimization results across controllers."""

    results = {}
    for file in result_files:
        with open(file, 'r') as f:
            data = json.load(f)
            controller_type = data['controller_type']
            results[controller_type] = data

    # Create comparison plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Plot 1: Best cost comparison
    controllers = list(results.keys())
    costs = [results[ctrl]['best_cost'] for ctrl in controllers]

    axes[0, 0].bar(controllers, costs)
    axes[0, 0].set_title('Best Cost Comparison')
    axes[0, 0].set_ylabel('Cost')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Plot 2: Convergence comparison
    for ctrl in controllers:
        if 'cost_history' in results[ctrl]:
            axes[0, 1].plot(results[ctrl]['cost_history'], label=ctrl)
    axes[0, 1].set_title('Convergence History')
    axes[0, 1].set_xlabel('Iteration')
    axes[0, 1].set_ylabel('Cost')
    axes[0, 1].legend()

    # Plot 3: Performance metrics
    metrics = ['ise', 'control_effort', 'control_rate', 'sliding_energy']
    x = np.arange(len(metrics))
    width = 0.2

    for i, ctrl in enumerate(controllers):
        if 'performance_metrics' in results[ctrl]:
            values = [results[ctrl]['performance_metrics'].get(m, 0) for m in metrics]
            axes[1, 0].bar(x + i*width, values, width, label=ctrl)

    axes[1, 0].set_title('Performance Metrics')
    axes[1, 0].set_xlabel('Metrics')
    axes[1, 0].set_xticks(x + width)
    axes[1, 0].set_xticklabels(metrics, rotation=45)
    axes[1, 0].legend()

    # Plot 4: Optimization info
    info_data = []
    for ctrl in controllers:
        info = results[ctrl]['optimization_info']
        info_data.append([
            info['n_iterations'],
            info.get('convergence_iteration', info['n_iterations']),
            info.get('final_diversity', 0)
        ])

    info_array = np.array(info_data)
    x = np.arange(len(controllers))

    axes[1, 1].bar(x - 0.2, info_array[:, 0], 0.4, label='Total Iterations')
    axes[1, 1].bar(x + 0.2, info_array[:, 1], 0.4, label='Convergence Iteration')
    axes[1, 1].set_title('Optimization Statistics')
    axes[1, 1].set_xlabel('Controller')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(controllers, rotation=45)
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig('optimization_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

    return results

# Usage example
result_files = [
    'classical_smc_optimized.json',
    'sta_smc_optimized.json',
    'adaptive_smc_optimized.json'
]

comparison = compare_optimization_results(result_files)