# Example from: docs\DOCUMENTATION_IMPLEMENTATION_PLAN.md
# Index: 3
# Runnable: False
# Hash: c1574c53

def compute_control(
    self,
    state: np.ndarray,
    state_vars: Dict[str, Any],
    history: Dict[str, np.ndarray]
) -> Tuple[float, Dict[str, Any], Dict[str, np.ndarray]]:
    """
    Compute control output using hybrid adaptive super-twisting SMC.

    Combines adaptive gain tuning with super-twisting algorithm for
    chattering reduction while maintaining robustness.

    Parameters
    ----------
    state : np.ndarray, shape (4,)
        Current system state [x, theta1, theta2, x_dot, theta1_dot, theta2_dot].
    state_vars : dict
        Controller internal state variables.
    history : dict
        Historical data for control computation.

    Returns
    -------
    u : float
        Control force in Newtons.
    updated_state_vars : dict
        Updated controller state variables.
    updated_history : dict
        Updated historical data.

    Notes
    -----
    The hybrid controller switches between adaptive and STA modes based on
    the magnitude of the sliding surface. See [1]_ for theoretical details.

    References
    ----------
    .. [1] Utkin, V., Guldner, J., & Shi, J. (2009). Sliding Mode Control
           in Electro-Mechanical Systems. CRC Press.

    Examples
    --------
    >>> controller = HybridAdaptiveSTASMC(gains=[...])
    >>> state = np.array([0.1, 0.05, 0.03, 0.0, 0.0, 0.0])
    >>> u, state_vars, history = controller.compute_control(state, {}, {})
    """