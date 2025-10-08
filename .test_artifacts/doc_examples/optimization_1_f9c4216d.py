# Example from: docs\guides\api\optimization.md
# Index: 1
# Runnable: True
# Hash: f9c4216d

from src.optimizer import PSOTuner
from src.controllers import SMCType, get_gain_bounds_for_pso

# Get recommended bounds for controller type
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# Initialize tuner
tuner = PSOTuner(
    controller_type=SMCType.CLASSICAL,
    bounds=bounds,
    n_particles=30,        # Swarm size
    iters=100,            # Number of iterations
    config=config         # Simulation configuration
)