# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 8
# Runnable: True
# Hash: 453c9ce8

from pyswarms.single import GlobalBestPSO
import numpy as np

def multi_objective_cost(gains_array):
    """
    Returns tuple: (performance_cost, energy_cost)
    PSO will optimize weighted sum, but we track both.
    """
    # Run simulation with candidate gains
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains_array)
    result = simulate(controller, duration=5.0, dt=0.01)

    # Compute both objectives
    performance_cost = result['metrics']['ise'] + result['metrics']['itae']
    energy_cost = result['metrics']['control_effort']

    # Weighted sum for PSO (user-defined trade-off)
    alpha = 0.7  # Performance weight
    combined_cost = alpha * performance_cost + (1 - alpha) * energy_cost

    return combined_cost, performance_cost, energy_cost

# Run PSO and track Pareto front
pareto_solutions = []

for alpha in [0.1, 0.3, 0.5, 0.7, 0.9]:  # Different trade-offs
    # Re-run PSO with different alpha
    best_gains, best_cost = run_pso_with_alpha(alpha)
    pareto_solutions.append({
        'alpha': alpha,
        'gains': best_gains,
        'performance': performance_cost,
        'energy': energy_cost
    })

# Visualize Pareto front
import matplotlib.pyplot as plt

perf = [s['performance'] for s in pareto_solutions]
energy = [s['energy'] for s in pareto_solutions]

plt.plot(perf, energy, 'bo-')
plt.xlabel('Performance Cost (ISE + ITAE)')
plt.ylabel('Energy Cost')
plt.title('Pareto Front: Performance vs Energy Trade-off')
plt.grid(True)
plt.show()