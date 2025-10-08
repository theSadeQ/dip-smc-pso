# Example from: docs\references\bibliography.md
# Index: 1
# Runnable: True
# Hash: 2718195f

def super_twisting_control(self, s: float) -> float:
    """
    Implements super-twisting algorithm from {cite}`levant2003higher`.

    Based on the theoretical development in {cite}`moreno2012strict`
    with Lyapunov analysis ensuring finite-time convergence.
    """
    return -self.alpha * np.abs(s)**0.5 * np.sign(s) - self.beta * np.sign(s)