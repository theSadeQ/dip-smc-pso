# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 5
# Runnable: False
# Hash: 6d54dd18

# example-metadata:
# runnable: false

class MPCConfig:
    """Configuration for Model Predictive Control (MPC) controller.

    Encapsulates MPC-specific parameters including prediction horizon,
    control horizon, and cost function weights.

    Parameters
    ----------
    prediction_horizon : int
        Number of future steps to predict (N).
    control_horizon : int
        Number of control moves to optimize (M). Must be <= prediction_horizon.
    Q : np.ndarray, shape (n_states, n_states)
        State error cost matrix.
    R : np.ndarray, shape (n_controls, n_controls)
        Control effort cost matrix.
    dt : float, default=0.01
        Time step for discretization (seconds).
    max_force : float, default=100.0
        Maximum control force constraint (N).

    Examples
    --------
    >>> config = MPCConfig(
    ...     prediction_horizon=20,
    ...     control_horizon=5,
    ...     Q=np.diag([10, 10, 5, 1, 1, 1]),
    ...     R=np.array([[0.1]]),
    ...     dt=0.01,
    ...     max_force=100.0
    ... )
    """