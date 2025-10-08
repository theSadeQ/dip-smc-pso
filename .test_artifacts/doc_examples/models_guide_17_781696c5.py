# Example from: docs\plant\models_guide.md
# Index: 17
# Runnable: True
# Hash: 781696c5

import numpy as np
from src.plant.models.simplified import SimplifiedDIPDynamics, SimplifiedDIPConfig

# Setup
config = SimplifiedDIPConfig.create_default()
dynamics = SimplifiedDIPDynamics(config, enable_fast_mode=True)

# Initial state (small perturbation from upright)
state = np.array([0.0, 0.1, -0.05, 0.0, 0.0, 0.0])

# Control input
control = np.array([5.0])  # 5 N force on cart

# Compute dynamics
result = dynamics.compute_dynamics(state, control, time=0.0)

if result.success:
    print(f"State derivative: {result.state_derivative}")
    print(f"Total energy: {result.info['total_energy']:.4f} J")
else:
    print(f"Computation failed: {result.info['failure_reason']}")