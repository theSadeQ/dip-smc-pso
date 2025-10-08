# Example from: docs\guides\api\optimization.md
# Index: 19
# Runnable: True
# Hash: 702248a1

def pareto_optimization(gains):
    """Return multiple objectives for Pareto analysis."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)

    return {
        'ise': result['metrics']['ise'],
        'energy': result['metrics']['control_effort'],
        'time': result['metrics']['settling_time']
    }

# Run PSO multiple times with different weights
pareto_front = []
weight_combinations = [
    (0.8, 0.1, 0.1),  # Prioritize ISE
    (0.5, 0.4, 0.1),  # Balance ISE and energy
    (0.3, 0.3, 0.4),  # Prioritize settling time
]

for w_ise, w_energy, w_time in weight_combinations:
    cost_fn = lambda g: multi_objective_cost(g, w_ise, w_energy, w_time)
    tuner = PSOTuner(SMCType.CLASSICAL, bounds, cost_function=cost_fn)
    gains, _ = tuner.optimize()

    metrics = pareto_optimization(gains)
    pareto_front.append({
        'gains': gains,
        'weights': (w_ise, w_energy, w_time),
        'metrics': metrics
    })

# Visualize Pareto front
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ise_vals = [p['metrics']['ise'] for p in pareto_front]
energy_vals = [p['metrics']['energy'] for p in pareto_front]
time_vals = [p['metrics']['time'] for p in pareto_front]

ax.scatter(ise_vals, energy_vals, time_vals)
ax.set_xlabel('ISE')
ax.set_ylabel('Energy')
ax.set_zlabel('Settling Time')
plt.title('Pareto Front: Multi-Objective Optimization')
plt.show()