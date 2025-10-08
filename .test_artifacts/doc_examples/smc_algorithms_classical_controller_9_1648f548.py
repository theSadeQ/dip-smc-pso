# Example from: docs\reference\controllers\smc_algorithms_classical_controller.md
# Index: 9
# Runnable: True
# Hash: 1648f548

from src.controllers.smc.algorithms.classical.boundary_layer import BoundaryLayer

# Experiment with different chattering reduction methods
boundary_layer = BoundaryLayer(
    epsilon=0.01,
    method='tanh',  # 'tanh', 'linear', 'sigmoid'
    slope=3.0       # Steepness parameter for tanh
)

# Custom configuration
config = ClassicalSMCConfig(
    surface_gains=[10.0, 8.0, 15.0, 12.0],
    switching_gain=50.0,
    derivative_gain=5.0,
    max_force=100.0,
    boundary_layer=0.01
)

controller = ClassicalSMC(config)