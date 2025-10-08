# Example from: docs\api\phase_4_3_progress_report.md
# Index: 1
# Runnable: False
# Hash: 7cb92bc9

def optimize_bounds_for_controller(
    self,
    controller_type: SMCType,
    strategy: BoundsOptimizationStrategy = BoundsOptimizationStrategy.HYBRID,
    max_optimization_time: float = 300.0
) -> BoundsValidationResult:
    """
    Optimize PSO parameter bounds for specific controller type.

    This method implements multi-strategy bounds optimization combining
    physics-based constraints, empirical performance data, and PSO convergence
    properties to find optimal parameter search spaces for each SMC controller type.

    Mathematical Foundation
    -----------------------
    Bounds optimization maximizes the objective function:

    $$J_{bounds}(b_{lower}, b_{upper}) = w_1 \cdot R_{conv} + w_2 \cdot Q_{final} + w_3 \cdot P_{success}$$

    where:
    - $R_{conv}$: Convergence rate improvement
    - $Q_{final}$: Final cost quality improvement
    - $P_{success}$: Success rate across trials
    - $w_1, w_2, w_3$: Strategy-dependent weights

    Algorithm
    ---------
    1. Generate candidate bounds from multiple strategies:
       - Physics-based: Controller stability constraints
       - Performance-driven: Empirical data analysis
       - Convergence-focused: PSO sensitivity analysis
    2. Evaluate candidates through PSO trials
    3. Select optimal bounds via multi-criteria scoring
    4. Validate through comprehensive testing

    Parameters
    ----------
    controller_type : SMCType
        Controller type to optimize bounds for (CLASSICAL, ADAPTIVE,
        SUPER_TWISTING, or HYBRID)
    strategy : BoundsOptimizationStrategy, optional
        Optimization strategy to use:
        - PHYSICS_BASED: Stability-constrained bounds
        - PERFORMANCE_DRIVEN: Empirically validated bounds
        - CONVERGENCE_FOCUSED: PSO-optimized bounds
        - HYBRID: Weighted combination (default)
    max_optimization_time : float, optional
        Maximum time allowed for optimization in seconds (default: 300.0)

    Returns
    -------
    BoundsValidationResult
        Comprehensive optimization results containing:
        - optimized_bounds: Tuple of (lower_bounds, upper_bounds)
        - improvement_ratio: Performance improvement factor
        - convergence_improvement: Convergence rate improvement percentage
        - performance_improvement: Final cost improvement percentage
        - validation_successful: Whether validation criteria were met
        - detailed_metrics: Full performance analysis

    Raises
    ------
    ValueError
        If controller_type is not supported or strategy is invalid
    TimeoutError
        If optimization exceeds max_optimization_time

    Examples
    --------
    >>> from src.optimization.validation.pso_bounds_optimizer import PSOBoundsOptimizer
    >>> from src.controllers.factory import SMCType
    >>>
    >>> optimizer = PSOBoundsOptimizer()
    >>> result = optimizer.optimize_bounds_for_controller(
    ...     controller_type=SMCType.CLASSICAL,
    ...     strategy=BoundsOptimizationStrategy.HYBRID,
    ...     max_optimization_time=300.0
    ... )
    >>> print(f"Improvement: {result.improvement_ratio:.2f}x")
    >>> print(f"Optimized bounds: {result.optimized_bounds}")

    See Also
    --------
    get_gain_bounds_for_pso : Retrieve current PSO bounds for controller type
    validate_smc_gains : Validate gain vector against constraints
    Phase 2.2 Documentation : PSO algorithm foundations (pso_algorithm_foundations.md)
    Phase 4.2 Documentation : Factory system API reference (factory_system_api_reference.md)

    References
    ----------
    .. [1] Kennedy, J., & Eberhart, R. (1995). "Particle Swarm Optimization."
    .. [2] Clerc, M., & Kennedy, J. (2002). "The Particle Swarm - Explosion,
           Stability, and Convergence in a Multidimensional Complex Space."

    Notes
    -----
    - Bounds optimization typically improves PSO convergence by 20-50%
    - Hybrid strategy recommended for production use
    - Optimization time scales with number of candidate bounds configurations
    - Results are deterministic given fixed random seed (seed=42)
    """