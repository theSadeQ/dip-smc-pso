# Example from: docs\optimization_simulation\guide.md
# Index: 20
# Runnable: True
# Hash: ae55feaf

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers import create_smc_for_pso, SMCType
from src.config import load_config
import numpy as np
import json

# 1. Load configuration
config = load_config("config.yaml")

# 2. Configure PSO for classical SMC
config.pso.n_particles = 40
config.pso.iters = 150
config.pso.bounds.classical_smc.min = [0.1, 0.1, 0.1, 0.1, 1.0, 0.0]
config.pso.bounds.classical_smc.max = [50.0, 50.0, 50.0, 50.0, 200.0, 50.0]

# 3. Define controller factory
def controller_factory(gains):
    return create_smc_for_pso(
        SMCType.CLASSICAL,
        gains,
        max_force=100.0,
        boundary_layer=0.01,
        dt=0.01
    )

# 4. Initialize PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42,
    instability_penalty_factor=100.0
)

# 5. Run optimization
result = tuner.optimise()

# 6. Extract and save results
best_gains = result['best_pos']
best_cost = result['best_cost']
cost_history = result['history']['cost']

# 7. Save optimized gains
gains_data = {
    "controller_type": "classical_smc",
    "gains": best_gains.tolist(),
    "cost": float(best_cost),
    "optimization_iterations": len(cost_history),
    "config": {
        "n_particles": config.pso.n_particles,
        "iters": config.pso.iters,
        "seed": 42
    }
}

with open("optimized_gains_classical.json", "w") as f:
    json.dump(gains_data, f, indent=2)

# 8. Validate optimized controller
from src.simulation.engines.simulation_runner import run_simulation
from src.plant.models.simplified import SimplifiedDIPDynamics

controller = controller_factory(best_gains)
dynamics = SimplifiedDIPDynamics(config.physics)
x0 = [0.0, 0.1, -0.05, 0.0, 0.0, 0.0]

t, x, u = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    sim_time=5.0,
    dt=0.01,
    initial_state=x0
)

print(f"Best gains: {best_gains}")
print(f"Best cost: {best_cost:.4f}")
print(f"Final state error: {np.linalg.norm(x[-1][:3]):.4f}")