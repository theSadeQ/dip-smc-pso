# Example from: docs\DOCUMENTATION_IMPLEMENTATION_PLAN.md
# Index: 2
# Runnable: False
# Hash: bb0bcf1b

# example-metadata:
# runnable: false

class MPCConfig:
    """
    Configuration dataclass for Model Predictive Controller.

    Encapsulates MPC-specific parameters including prediction horizon,
    control horizon, and constraint matrices.

    Parameters
    ----------
    prediction_horizon : int
        Number of steps to predict ahead (N).
    control_horizon : int
        Number of control moves to optimize (M).
    Q : np.ndarray
        State cost matrix (n x n).
    R : np.ndarray
        Control cost matrix (m x m).

    Attributes
    ----------
    N : int
        Prediction horizon.
    M : int
        Control horizon.

    Examples
    --------
    >>> config = MPCConfig(prediction_horizon=10, control_horizon=5, Q=np.eye(4), R=np.eye(1))
    >>> print(config.N)
    10
    """