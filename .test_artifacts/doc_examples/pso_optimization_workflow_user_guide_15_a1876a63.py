# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 15
# Runnable: False
# Hash: a1876a63

def analyze_convergence(cost_history, window_size=10):
    """Analyze PSO convergence characteristics."""

    analysis = {}

    # Convergence rate
    if len(cost_history) > window_size:
        recent_improvement = cost_history[-window_size] - cost_history[-1]
        analysis['improvement_rate'] = recent_improvement / window_size

    # Stagnation detection
    if len(cost_history) > 20:
        recent_costs = cost_history[-20:]
        stagnation = np.std(recent_costs) < 0.001
        analysis['is_stagnant'] = stagnation

    # Convergence quality
    final_cost = cost_history[-1]
    if final_cost < 50:
        analysis['convergence_quality'] = 'excellent'
    elif final_cost < 100:
        analysis['convergence_quality'] = 'good'
    elif final_cost < 200:
        analysis['convergence_quality'] = 'acceptable'
    else:
        analysis['convergence_quality'] = 'poor'

    return analysis

# Analyze optimization results
convergence_analysis = analyze_convergence(results['cost_history'])
print(f"Convergence Quality: {convergence_analysis['convergence_quality']}")