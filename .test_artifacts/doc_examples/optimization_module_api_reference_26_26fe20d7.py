# Example from: docs\api\optimization_module_api_reference.md
# Index: 26
# Runnable: False
# Hash: 26fe20d7

# example-metadata:
# runnable: false

def optimize_hyperparameters(
    self,
    controller_type: SMCType,
    objective: OptimizationObjective = OptimizationObjective.MULTI_OBJECTIVE,
    max_evaluations: int = 100,
    n_trials_per_evaluation: int = 5
) -> OptimizationResult:
    """
    Optimize PSO hyperparameters for specific controller type.

    Uses differential evolution to find optimal PSO parameters that
    minimize the selected objective function.

    Parameters
    ----------
    controller_type : SMCType
        Controller type to optimize hyperparameters for
    objective : OptimizationObjective, optional
        Optimization objective (default: MULTI_OBJECTIVE)
    max_evaluations : int, optional
        Maximum DE evaluations (default: 100)
    n_trials_per_evaluation : int, optional
        PSO trials per hyperparameter configuration (default: 5)

    Returns
    -------
    OptimizationResult
        Optimized hyperparameters with performance metrics
    """