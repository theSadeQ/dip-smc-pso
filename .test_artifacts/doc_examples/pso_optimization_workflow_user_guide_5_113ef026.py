# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 5
# Runnable: True
# Hash: 113ef026

import numpy as np
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import ControllerFactory

# Custom bounds for aggressive tuning
custom_bounds = {
    'lower': np.array([1.0, 1.0, 1.0, 1.0, 5.0, 0.5]),
    'upper': np.array([25.0, 25.0, 25.0, 25.0, 150.0, 15.0])
}

# Create factory and run optimization
def create_controller(gains):
    return ControllerFactory.create_controller('classical_smc', gains)

pso_tuner = PSOTuner(create_controller, config, seed=42)
results = pso_tuner.optimize(
    bounds=(custom_bounds['lower'], custom_bounds['upper']),
    n_particles=75,
    n_iterations=150
)