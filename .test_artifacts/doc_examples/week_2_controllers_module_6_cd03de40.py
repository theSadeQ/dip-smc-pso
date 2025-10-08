# Example from: docs\plans\documentation\week_2_controllers_module.md
# Index: 6
# Runnable: True
# Hash: cd03de40

from src.controllers.smc import ClassicalSMC

controller = ClassicalSMC(
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0,
    boundary_layer=0.01
)