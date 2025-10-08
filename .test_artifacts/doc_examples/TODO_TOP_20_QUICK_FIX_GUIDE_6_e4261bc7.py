# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 6
# Runnable: False
# Hash: e4261bc7

# example-metadata:
# runnable: false

class UnavailableMPCConfig:
    """Placeholder configuration when MPC dependencies are unavailable.

    Raises informative error messages when MPC is requested but required
    libraries (CVXPY, OSQP) are not installed.

    Raises
    ------
    ImportError
        When attempting to create MPC controller without required dependencies.

    Notes
    -----
    To enable MPC: pip install cvxpy osqp
    """