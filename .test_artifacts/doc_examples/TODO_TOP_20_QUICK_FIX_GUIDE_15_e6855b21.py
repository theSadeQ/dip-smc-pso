# Example from: docs\TODO_TOP_20_QUICK_FIX_GUIDE.md
# Index: 15
# Runnable: False
# Hash: e6855b21

# example-metadata:
# runnable: false

class OptimizationResult:
    """Container for optimization algorithm results.

    Stores optimized parameters, convergence metrics, and optimization history.

    Attributes
    ----------
    best_params : np.ndarray
        Optimized parameter vector.
    best_cost : float
        Final cost function value.
    converged : bool
        Whether optimization converged to tolerance.
    iterations : int
        Number of iterations performed.
    history : Dict[str, List]
        Optimization history (cost, params per iteration).

    Examples
    --------
    >>> result = optimizer.optimize(objective_fn, bounds)
    >>> if result.converged:
    ...     controller = create_controller(gains=result.best_params)
    """