# Example from: docs\reference\optimization\algorithms_pso_optimizer.md
# Index: 7
# Runnable: True
# Hash: c66e4768

import matplotlib.pyplot as plt

# Track convergence history
convergence_history = []

def convergence_callback(iteration, global_best_cost):
    convergence_history.append(global_best_cost)
    print(f"Iteration {iteration}: Best cost = {global_best_cost:.6f}")

pso = PSOTuner(
    controller_factory=lambda g: create_smc_for_pso(SMCType.CLASSICAL, g),
    bounds=(bounds_lower, bounds_upper),
    callback=convergence_callback
)

best_gains, _ = pso.optimize()

# Plot convergence
plt.plot(convergence_history)
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.title('PSO Convergence Analysis')
plt.grid(True)
plt.show()