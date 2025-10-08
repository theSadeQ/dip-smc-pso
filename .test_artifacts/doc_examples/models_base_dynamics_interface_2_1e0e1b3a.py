# Example from: docs\reference\plant\models_base_dynamics_interface.md
# Index: 2
# Runnable: True
# Hash: 1e0e1b3a

class SMCController:
    def __init__(self, dynamics: DynamicsInterface):
        self.dynamics = dynamics  # Works with any implementation