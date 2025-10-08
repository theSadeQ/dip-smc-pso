# Example from: docs\reference\plant\models_base_dynamics_interface.md
# Index: 1
# Runnable: True
# Hash: bb0c14de

class DynamicsInterface(ABC):
    @abstractmethod
    def step(self, x: np.ndarray, u: np.ndarray, t: float) -> np.ndarray:
        """Compute state derivative dx/dt = f(x, u, t)."""
        pass

    @abstractmethod
    def get_linearization(self, x_eq: np.ndarray, u_eq: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute Jacobian matrices A, B at equilibrium."""
        pass