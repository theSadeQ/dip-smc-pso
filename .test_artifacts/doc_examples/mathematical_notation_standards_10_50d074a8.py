# Example from: docs\examples\mathematical_notation_standards.md
# Index: 10
# Runnable: False
# Hash: 50d074a8

# example-metadata:
# runnable: false

def compute_sliding_surface(self, state: np.ndarray, target: np.ndarray) -> float:
    """Compute the sliding surface value for classical SMC.

    The sliding surface is defined as:
    s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂

    where:
    - e₁, e₂: position errors for pendulum 1 and 2
    - ė₁, ė₂: velocity errors for pendulum 1 and 2
    - λ₁, λ₂: sliding surface gains (must be positive)

    Mathematical Background:
    The sliding surface design ensures that once the system reaches
    the surface (s=0), it will remain on the surface and converge
    to the desired equilibrium point in finite time.

    Parameters
    ----------
    state : np.ndarray, shape (6,)
        Current system state [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
    target : np.ndarray, shape (6,)
        Target state (typically upright equilibrium [0, 0, 0, 0, 0, 0])

    Returns
    -------
    float
        Sliding surface value. System is on sliding surface when s = 0.

    References
    ----------
    .. [1] Utkin, V. "Sliding Modes in Control and Optimization", 1992
    .. [2] Edwards, C. "Sliding Mode Control: Theory and Applications", 1998
    """