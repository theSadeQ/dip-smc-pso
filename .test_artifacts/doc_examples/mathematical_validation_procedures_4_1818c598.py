# Example from: docs\mathematical_validation_procedures.md
# Index: 4
# Runnable: False
# Hash: 1818c598

# example-metadata:
# runnable: false

def validate_pso_convergence_properties(pso_optimizer: PSOOptimizer,
                                       benchmark_functions: List[BenchmarkFunction]) -> PSOConvergenceValidationResult:
    """
    Validate PSO convergence properties using benchmark functions.

    Mathematical Foundation:
    - Clerc-Kennedy convergence conditions
    - Global convergence analysis
    - Convergence rate estimation
    """

    convergence_results = []

    for benchmark_func in benchmark_functions:
        # Run multiple PSO trials
        trial_results = []

        for trial in range(NUM_PSO_TRIALS):
            # Initialize PSO with validated parameters
            pso_result = pso_optimizer.optimize(
                objective_function=benchmark_func.objective,
                bounds=benchmark_func.bounds,
                max_iterations=MAX_PSO_ITERATIONS
            )

            # Analyze convergence properties
            convergence_analysis = _analyze_pso_convergence(
                pso_result.cost_history,
                benchmark_func.global_minimum,
                pso_result.final_cost
            )

            trial_results.append(convergence_analysis)

        # Aggregate trial results
        success_rate = len([r for r in trial_results if r.converged_to_global]) / len(trial_results)
        average_convergence_rate = np.mean([r.convergence_rate for r in trial_results if r.converged])

        convergence_results.append(PSOBenchmarkResult(
            benchmark_function=benchmark_func.name,
            success_rate=success_rate,
            average_convergence_rate=average_convergence_rate,
            trial_results=trial_results,
            mathematical_properties=_analyze_mathematical_properties(trial_results)
        ))

    return PSOConvergenceValidationResult(
        benchmark_results=convergence_results,
        overall_convergence_validated=all(r.success_rate >= MIN_PSO_SUCCESS_RATE for r in convergence_results),
        mathematical_interpretation=_interpret_pso_convergence(convergence_results)
    )

def _analyze_pso_convergence(cost_history: List[float],
                           global_minimum: float,
                           final_cost: float) -> ConvergenceAnalysis:
    """Analyze PSO convergence characteristics."""

    # Check if converged to global minimum
    convergence_tolerance = abs(global_minimum) * 0.01 if global_minimum != 0 else 0.01
    converged_to_global = abs(final_cost - global_minimum) < convergence_tolerance

    # Estimate convergence rate
    if len(cost_history) > 10:
        # Fit exponential decay model: cost(t) = A * exp(-λt) + C
        log_costs = np.log(np.array(cost_history) - global_minimum + 1e-8)
        convergence_rate = -np.polyfit(range(len(log_costs)), log_costs, 1)[0]
    else:
        convergence_rate = 0.0

    # Detect premature convergence
    cost_variance = np.var(cost_history[-10:]) if len(cost_history) >= 10 else float('inf')
    premature_convergence = cost_variance < PREMATURE_CONVERGENCE_THRESHOLD and not converged_to_global

    return ConvergenceAnalysis(
        converged=final_cost <= global_minimum + convergence_tolerance,
        converged_to_global=converged_to_global,
        convergence_rate=convergence_rate,
        premature_convergence=premature_convergence,
        final_error=abs(final_cost - global_minimum)
    )