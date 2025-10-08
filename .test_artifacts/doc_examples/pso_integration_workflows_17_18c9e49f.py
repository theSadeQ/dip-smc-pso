# Example from: docs\technical\pso_integration_workflows.md
# Index: 17
# Runnable: True
# Hash: 18c9e49f

def analyze_optimization_history(optimization_result):
    """Analyze optimization history and performance trends."""

    if not optimization_result['success']:
        return

    history = optimization_result.get('convergence_history', {})
    cost_history = history.get('cost', [])

    if len(cost_history) == 0:
        print("No history available for analysis")
        return

    import numpy as np
    import matplotlib.pyplot as plt

    costs = np.array(cost_history)
    iterations = np.arange(len(costs))

    # Plot convergence history
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(iterations, costs, 'b-', linewidth=2)
    plt.xlabel('Iteration')
    plt.ylabel('Best Cost')
    plt.title('PSO Convergence History')
    plt.grid(True)

    # Plot improvement rate
    plt.subplot(2, 2, 2)
    if len(costs) > 1:
        improvement = np.diff(costs)
        plt.plot(iterations[1:], improvement, 'r-', linewidth=1)
        plt.xlabel('Iteration')
        plt.ylabel('Cost Improvement')
        plt.title('Cost Improvement Rate')
        plt.grid(True)

    # Plot convergence rate
    plt.subplot(2, 2, 3)
    window_size = min(10, len(costs) // 4)
    if window_size > 1:
        convergence_rate = np.array([
            np.std(costs[max(0, i-window_size):i+1]) / max(np.mean(costs[max(0, i-window_size):i+1]), 1e-6)
            for i in range(window_size, len(costs))
        ])
        plt.plot(iterations[window_size:], convergence_rate, 'g-', linewidth=2)
        plt.xlabel('Iteration')
        plt.ylabel('Convergence Rate')
        plt.title('Convergence Rate (std/mean)')
        plt.yscale('log')
        plt.grid(True)

    # Summary statistics
    plt.subplot(2, 2, 4)
    final_cost = costs[-1]
    initial_cost = costs[0]
    improvement_ratio = (initial_cost - final_cost) / max(initial_cost, 1e-6)

    stats_text = f"""
    Initial Cost: {initial_cost:.6f}
    Final Cost: {final_cost:.6f}
    Improvement: {improvement_ratio:.1%}
    Iterations: {len(costs)}
    """

    plt.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center')
    plt.axis('off')
    plt.title('Optimization Summary')

    plt.tight_layout()
    plt.savefig('pso_convergence_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    return {
        'initial_cost': float(initial_cost),
        'final_cost': float(final_cost),
        'improvement_ratio': float(improvement_ratio),
        'iterations': len(costs)
    }

# Usage example
result = pso_factory.optimize_controller()
history_analysis = analyze_optimization_history(result)