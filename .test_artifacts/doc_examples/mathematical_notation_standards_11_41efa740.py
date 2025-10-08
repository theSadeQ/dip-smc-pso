# Example from: docs\examples\mathematical_notation_standards.md
# Index: 11
# Runnable: False
# Hash: 41efa740

# example-metadata:
# runnable: false

class ClassicalSMC:
    """Classical Sliding Mode Controller for double-inverted pendulum.

    Implements the classical SMC algorithm with boundary layer for chattering
    reduction. The control law consists of equivalent control and switching
    control components:

    u = u_eq + u_sw

    where:
    - u_eq: Equivalent control (model-based feedforward)
    - u_sw: Switching control (robust feedback)

    The sliding surface is designed as:
    s = λ₁e₁ + λ₂e₂ + ė₁ + ė₂

    Stability is guaranteed when λ₁, λ₂ > 0, ensuring the characteristic
    polynomial s² + λ₂s + λ₁ = 0 has stable roots.

    Parameters
    ----------
    gains : List[float]
        Controller gains [k₁, k₂, λ₁, λ₂, K, k_d] where:
        - k₁, k₂: Position feedback gains
        - λ₁, λ₂: Sliding surface gains
        - K: Switching gain
        - k_d: Derivative gain
    max_force : float
        Maximum control force (saturation limit)
    boundary_layer : float
        Boundary layer thickness for chattering reduction

    Attributes
    ----------
    n_gains : int
        Number of controller gains (6 for classical SMC)

    Examples
    --------
    >>> controller = ClassicalSMC(
    ...     gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0],
    ...     max_force=100.0,
    ...     boundary_layer=0.01
    ... )
    >>> state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
    >>> result = controller.compute_control(state, None, {})
    >>> print(f"Control output: {result['u']:.4f}")
    """