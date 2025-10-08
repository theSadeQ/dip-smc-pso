# Example from: docs\implementation\legacy_index.md
# Index: 3
# Runnable: False
# Hash: c0d1d6c2

# example-metadata:
# runnable: false

class ControlSystemError(Exception):
    """Base exception for control system errors."""
    pass

class NumericalInstabilityError(ControlSystemError):
    """Raised when numerical instability detected."""

    def __init__(self, t: float, x: np.ndarray):
        super().__init__(
            f"Numerical instability at t={t:.3f}, "
            f"max(|x|)={np.max(np.abs(x)):.2e}"
        )
        self.time = t
        self.state = x.copy()

class ConvergenceError(ControlSystemError):
    """Raised when optimization fails to converge."""
    pass