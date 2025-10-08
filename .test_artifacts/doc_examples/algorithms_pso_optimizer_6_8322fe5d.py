# Example from: docs\reference\optimization\algorithms_pso_optimizer.md
# Index: 6
# Runnable: True
# Hash: 8322fe5d

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import create_smc_for_pso, SMCType

# Define multi-objective cost function
def multi_objective_cost(gains):
    controller = create_smc_for_pso(SMCType.HYBRID, gains)
    result = simulate(controller, duration=10.0)

    # Combine objectives with weights
    tracking_error = np.mean(np.abs(result.states[:, :2]))  # Angles
    control_effort = np.mean(np.abs(result.control))
    chattering = np.std(np.diff(result.control))

    return 0.6 * tracking_error + 0.3 * control_effort + 0.1 * chattering

# Configure PSO with adaptive parameters
pso = PSOTuner(
    controller_factory=lambda g: create_smc_for_pso(SMCType.HYBRID, g),
    bounds=([1.0]*4, [50.0]*4),  # Hybrid has 4 gains
    n_particles=40,
    max_iter=100,
    w=0.7,           # Inertia weight
    c1=1.5,          # Cognitive coefficient
    c2=1.5           # Social coefficient
)

best_gains, best_cost = pso.optimize()
print(f"Optimal gains: {best_gains}, Cost: {best_cost:.4f}")