# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 13
# Runnable: False
# Hash: f9c827a1

# example-metadata:
# runnable: false

def compute_sliding_surface(self, state: np.ndarray, target: np.ndarray) -> float:
    """Compute sliding surface value for classical SMC.

    Mathematical Foundation:
    The sliding surface is defined as:
    s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂

    where:
    - e₁, e₂: position errors for pendulum 1 and 2
    - ė₁, ė₂: velocity errors for pendulum 1 and 2
    - λ₁, λ₂: sliding surface gains (must be positive)

    Stability Analysis:
    The sliding surface design ensures that once the system reaches
    the surface (s=0), it will remain on the surface and converge
    to the desired equilibrium point according to the dynamics:

    ë₁ + λ₁ė₁ + c₁e₁ = 0
    ë₂ + λ₂ė₂ + c₂e₂ = 0

    Parameters
    ----------
    state : np.ndarray, shape (6,)
        Current system state [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
    target : np.ndarray, shape (6,)
        Target state (typically upright equilibrium)

    Returns
    -------
    float
        Sliding surface value. System is on sliding surface when s = 0.

    Raises
    ------
    ValueError
        If state or target arrays have incorrect dimensions

    References
    ----------
    .. [1] Utkin, V. "Sliding Modes in Control and Optimization", 1992
    .. [2] Edwards, C. "Sliding Mode Control: Theory and Applications", 1998

    Examples
    --------
    >>> controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5])
    >>> state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
    >>> target = np.zeros(6)
    >>> surface_value = controller.compute_sliding_surface(state, target)
    >>> print(f"Sliding surface value: {surface_value:.4f}")
    """