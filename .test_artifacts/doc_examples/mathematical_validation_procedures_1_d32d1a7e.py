# Example from: docs\mathematical_validation_procedures.md
# Index: 1
# Runnable: False
# Hash: d32d1a7e

# example-metadata:
# runnable: false

def validate_lyapunov_stability(controller: SMCController,
                              test_scenarios: List[TestScenario]) -> LyapunovValidationResult:
    """
    Validate Lyapunov stability condition for SMC controller.

    Mathematical Verification:
    - Verifies V̇(s) = s·ṡ < 0 for all s ≠ 0
    - Tests across representative state space
    - Validates finite-time convergence properties

    Parameters
    ----------
    controller : SMCController
        Controller instance to validate
    test_scenarios : List[TestScenario]
        Representative test scenarios covering state space

    Returns
    -------
    LyapunovValidationResult
        Comprehensive stability validation results
    """

    validation_results = []
    stability_violations = []

    for scenario in test_scenarios:
        # Generate state trajectory
        t, states = simulate_scenario(controller, scenario)

        for i, state in enumerate(states):
            # Compute sliding surface value
            s = controller.compute_sliding_surface(state, scenario.target)

            # Skip points on sliding surface (within tolerance)
            if abs(s) < SLIDING_SURFACE_TOLERANCE:
                continue

            # Compute sliding surface derivative
            s_dot = controller.compute_surface_derivative(state, scenario.target)

            # Lyapunov stability condition: V̇ = s·ṡ < 0
            v_dot = s * s_dot

            if v_dot >= 0:
                stability_violations.append(StabilityViolation(
                    scenario=scenario.name,
                    time=t[i],
                    state=state,
                    sliding_surface=s,
                    surface_derivative=s_dot,
                    lyapunov_derivative=v_dot,
                    violation_magnitude=v_dot
                ))

            validation_results.append(LyapunovTestPoint(
                scenario=scenario.name,
                time=t[i],
                sliding_surface=s,
                lyapunov_derivative=v_dot,
                stable=v_dot < 0
            ))

    # Calculate stability metrics
    total_points = len(validation_results)
    stable_points = len([r for r in validation_results if r.stable])
    stability_percentage = (stable_points / total_points) * 100 if total_points > 0 else 0

    return LyapunovValidationResult(
        total_test_points=total_points,
        stable_points=stable_points,
        stability_percentage=stability_percentage,
        stability_violations=stability_violations,
        validation_status='passed' if not stability_violations else 'failed',
        mathematical_interpretation=_interpret_lyapunov_results(stability_percentage, stability_violations)
    )

def _interpret_lyapunov_results(stability_percentage: float,
                               violations: List[StabilityViolation]) -> str:
    """Generate mathematical interpretation of Lyapunov stability results."""

    if stability_percentage >= 99.9:
        return "Lyapunov stability condition satisfied across test space. Controller theoretically stable."
    elif stability_percentage >= 95.0:
        interpretation = f"Lyapunov stability satisfied for {stability_percentage:.1f}% of test points. "
        if violations:
            violation_regions = _analyze_violation_regions(violations)
            interpretation += f"Violations concentrated in {violation_regions}. Consider gain tuning."
        return interpretation
    else:
        return f"Significant Lyapunov stability violations ({100-stability_percentage:.1f}%). Controller stability not verified."