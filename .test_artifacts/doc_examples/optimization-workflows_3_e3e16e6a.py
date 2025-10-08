# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 3
# Runnable: True
# Hash: e3e16e6a

def pareto_cost(metrics, config, alpha=0.5):
    """
    Pareto front exploration: performance vs efficiency.

    alpha=0.0: Pure efficiency (low control effort)
    alpha=1.0: Pure performance (low ISE)
    alpha=0.5: Balanced trade-off
    """
    # Normalize metrics to [0, 1] range
    performance_cost = metrics['ise'] / 2.0  # Assume ISE < 2.0
    efficiency_cost = metrics['control_effort'] / 500.0  # Assume effort < 500

    # Weighted combination
    cost = alpha * performance_cost + (1 - alpha) * efficiency_cost

    return cost

# Run PSO for multiple alpha values
alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
pareto_solutions = []

for alpha in alphas:
    custom_cost = lambda m, c: pareto_cost(m, c, alpha=alpha)

    tuner = PSOTuner(
        controller_type='classical_smc',
        config=config,
        cost_function=custom_cost
    )

    gains, cost = tuner.optimize()

    # Re-evaluate to get actual metrics
    result = evaluate_controller(gains)

    pareto_solutions.append({
        'alpha': alpha,
        'gains': gains,
        'ise': result['metrics']['ise'],
        'control_effort': result['metrics']['control_effort']
    })

# Plot Pareto front
import matplotlib.pyplot as plt

ise_values = [sol['ise'] for sol in pareto_solutions]
effort_values = [sol['control_effort'] for sol in pareto_solutions]

plt.plot(ise_values, effort_values, 'bo-')
plt.xlabel('ISE (Performance)')
plt.ylabel('Control Effort (Energy)')
plt.title('Pareto Front: Performance vs Efficiency')
plt.grid(True)
plt.show()