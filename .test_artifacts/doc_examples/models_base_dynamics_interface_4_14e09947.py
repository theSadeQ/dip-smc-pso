# Example from: docs\reference\plant\models_base_dynamics_interface.md
# Index: 4
# Runnable: True
# Hash: 14e09947

class MockDynamics(DynamicsInterface):
    def step(self, x, u, t):
        return np.zeros_like(x)  # Trivial for testing