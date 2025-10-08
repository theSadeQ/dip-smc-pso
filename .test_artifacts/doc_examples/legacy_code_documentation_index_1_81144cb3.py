# Example from: docs\implementation\legacy_code_documentation_index.md
# Index: 1
# Runnable: False
# Hash: 81144cb3

# example-metadata:
# runnable: false

def compute_control(self, x: np.ndarray, x_ref: np.ndarray, t: float) -> float:
    """
    Compute sliding mode control input.

    Implements the classical SMC law from {eq}`classical_smc_structure`:

    .. math::
        u(t) = u_{eq}(t) + u_{sw}(t)

    where equivalent control ensures sliding surface convergence.

    Parameters
    ----------
    x : np.ndarray, shape (6,)
        Current state vector [x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂]
    x_ref : np.ndarray, shape (6,)
        Reference trajectory
    t : float
        Current time

    Returns
    -------
    u : float
        Control force (N)

    Notes
    -----
    The sliding surface is defined as in {eq}`linear_sliding_surface`.
    Stability is guaranteed by Theorem 3 in {doc}`../theory/smc_theory_complete`.

    Examples
    --------
    >>> controller = ClassicalSMC(c=[5, 8, 7], eta=2.0, epsilon=0.1)
    >>> x = np.array([0.1, 0.05, 0.02, 0, 0, 0])
    >>> x_ref = np.zeros(6)
    >>> u = controller.compute_control(x, x_ref, 0.0)
    >>> print(f"Control input: {u:.3f} N")
    Control input: -1.234 N

    See Also
    --------
    theory.smc_theory_complete : Mathematical foundations
    sta_smc.SuperTwistingSMC : Alternative SMC implementation
    """