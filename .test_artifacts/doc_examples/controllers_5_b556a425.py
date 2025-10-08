# Example from: docs\guides\api\controllers.md
# Index: 5
# Runnable: True
# Hash: b556a425

from src.controllers import get_gain_bounds_for_pso

# Get recommended bounds for each controller type
bounds_classical = get_gain_bounds_for_pso(SMCType.CLASSICAL)
# Returns: [(0.1, 50), (0.1, 50), (0.1, 50), (0.1, 50), (1.0, 200), (0.0, 50)]

bounds_adaptive = get_gain_bounds_for_pso(SMCType.ADAPTIVE)
# Returns: [(0.1, 50), (0.1, 50), (0.1, 50), (0.1, 50), (0.01, 10)]

# Use with PSO
from src.optimizer import PSOTuner

tuner = PSOTuner(
    controller_type=SMCType.CLASSICAL,
    bounds=bounds_classical,
    n_particles=30,
    iters=100
)