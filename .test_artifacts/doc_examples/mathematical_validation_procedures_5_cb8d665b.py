# Example from: docs\mathematical_validation_procedures.md
# Index: 5
# Runnable: False
# Hash: cb8d665b

# example-metadata:
# runnable: false

def validate_multi_objective_pso(multi_obj_optimizer: MultiObjectivePSOOptimizer,
                               test_problems: List[MultiObjectiveTestProblem]) -> MultiObjectiveValidationResult:
    """
    Validate multi-objective PSO using standard test problems.

    Mathematical Foundation:
    - Pareto optimality verification
    - Hypervolume indicator calculation
    - Convergence to Pareto front analysis
    """

    validation_results = []

    for test_problem in test_problems:
        # Run multi-objective optimization
        pareto_result = multi_obj_optimizer.optimize(
            objective_functions=test_problem.objectives,
            bounds=test_problem.bounds,
            max_iterations=MAX_MULTI_OBJ_ITERATIONS
        )

        # Validate Pareto optimality
        pareto_validation = _validate_pareto_optimality(
            pareto_result.pareto_front,
            test_problem.true_pareto_front
        )

        # Calculate hypervolume indicator
        hypervolume = _calculate_hypervolume(
            pareto_result.pareto_front,
            test_problem.reference_point
        )

        # Analyze convergence to Pareto front
        convergence_analysis = _analyze_pareto_convergence(
            pareto_result.pareto_history,
            test_problem.true_pareto_front
        )

        validation_results.append(MultiObjectiveTestResult(
            test_problem=test_problem.name,
            pareto_validation=pareto_validation,
            hypervolume=hypervolume,
            convergence_analysis=convergence_analysis,
            mathematical_properties=_analyze_multi_objective_properties(pareto_result)
        ))

    return MultiObjectiveValidationResult(
        test_results=validation_results,
        overall_validation=all(r.pareto_validation.valid for r in validation_results),
        mathematical_interpretation=_interpret_multi_objective_results(validation_results)
    )