# Example from: docs\api\optimization_module_api_reference.md
# Index: 22
# Runnable: False
# Hash: b37c0c28

def optimize_bounds_for_controller(
    self,
    controller_type: SMCType,
    strategy: BoundsOptimizationStrategy = BoundsOptimizationStrategy.HYBRID,
    max_optimization_time: float = 300.0,
    n_trials: int = 10
) -> BoundsValidationResult:
    """
    Optimize PSO parameter bounds for specific controller type.

    Algorithm:
    1. Generate candidate bounds from selected strategy
    2. Evaluate candidates through PSO trials
    3. Score candidates using multi-criteria objective
    4. Select optimal bounds via Pareto dominance
    5. Validate through comprehensive testing

    Parameters
    ----------
    controller_type : SMCType
        Controller type to optimize bounds for
    strategy : BoundsOptimizationStrategy, optional
        Optimization strategy (default: HYBRID)
    max_optimization_time : float, optional
        Maximum time in seconds (default: 300)
    n_trials : int, optional
        Number of PSO trials per candidate (default: 10)

    Returns
    -------
    BoundsValidationResult
        Optimized bounds with performance metrics
    """