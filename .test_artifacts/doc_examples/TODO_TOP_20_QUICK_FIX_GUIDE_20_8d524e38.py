# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 20
# Runnable: False
# Hash: 8d524e38

# example-metadata:
# runnable: false

class ControllerState:
    """Container for controller internal state.

    Stores controller state variables for adaptive and hybrid controllers
    that maintain internal state between control steps.

    Attributes
    ----------
    adaptive_gains : np.ndarray, optional
        Adaptive gain estimates.
    integral_error : float
        Accumulated integral error.
    previous_control : float
        Previous control output (for rate limiting).
    history : Dict[str, List]
        Controller history buffers.

    Examples
    --------
    >>> state = ControllerState()
    >>> control, state = controller.compute_control(system_state, state)
    """