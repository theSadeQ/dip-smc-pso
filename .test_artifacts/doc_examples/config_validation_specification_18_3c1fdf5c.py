# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 18
# Runnable: True
# Hash: 3c1fdf5c

class DynamicsModel:
    def compute_dynamics(self, state: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Return (F, B) where ẋ = F(x) + B(x)u"""
        pass

    def get_mass_matrix(self, state: np.ndarray) -> np.ndarray:
        """Return mass matrix M(x)"""
        pass