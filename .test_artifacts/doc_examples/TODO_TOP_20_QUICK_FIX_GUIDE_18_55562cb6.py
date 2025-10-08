# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 18
# Runnable: False
# Hash: 55562cb6

class DynamicsModelProtocol:
    """Protocol defining interface for dynamics models.

    All dynamics implementations (simplified, full, low-rank) must implement
    this interface for compatibility with simulation engine.

    Methods
    -------
    derivatives(state: np.ndarray, control: float) -> np.ndarray
        Compute state derivatives dx/dt = f(x, u).
    linearize(state: np.ndarray) -> Tuple[np.ndarray, np.ndarray]
        Compute linearized A, B matrices at given state.
    """