# Example from: docs\mathematical_validation_procedures.md
# Index: 2
# Runnable: False
# Hash: 5af34ea7

def validate_sliding_surface_reachability(controller: SMCController,
                                        test_scenarios: List[TestScenario]) -> ReachabilityValidationResult:
    """
    Validate sliding surface reachability condition.

    Mathematical Foundation:
    Reachability condition: s·ṡ ≤ -η|s| where η > 0

    Finite-time reaching: t_reach ≤ |s₀|/η
    """

    reachability_results = []

    for scenario in test_scenarios:
        initial_state = scenario.initial_state
        target_state = scenario.target_state

        # Compute initial sliding surface value
        s0 = controller.compute_sliding_surface(initial_state, target_state)

        if abs(s0) < SLIDING_SURFACE_TOLERANCE:
            # Already on sliding surface
            continue

        # Simulate trajectory to sliding surface
        t, states = simulate_to_sliding_surface(controller, scenario)

        # Find reaching time
        reaching_time = None
        for i, state in enumerate(states):
            s = controller.compute_sliding_surface(state, target_state)
            if abs(s) < SLIDING_SURFACE_TOLERANCE:
                reaching_time = t[i]
                break

        # Validate reachability condition along trajectory
        reachability_condition_satisfied = True
        reaching_rate_violations = []

        for i, state in enumerate(states):
            if reaching_time and t[i] > reaching_time:
                break  # Stop after reaching sliding surface

            s = controller.compute_sliding_surface(state, target_state)
            s_dot = controller.compute_surface_derivative(state, target_state)

            # Reachability condition: s·ṡ ≤ -η|s|
            reaching_condition = s * s_dot
            required_reaching_rate = -controller.reaching_rate * abs(s)

            if reaching_condition > required_reaching_rate:
                reachability_condition_satisfied = False
                reaching_rate_violations.append(ReachingRateViolation(
                    time=t[i],
                    state=state,
                    sliding_surface=s,
                    surface_derivative=s_dot,
                    reaching_condition=reaching_condition,
                    required_rate=required_reaching_rate
                ))

        # Theoretical reaching time bound
        theoretical_reaching_time = abs(s0) / controller.reaching_rate if controller.reaching_rate > 0 else float('inf')

        reachability_results.append(ReachabilityTestResult(
            scenario=scenario.name,
            initial_sliding_surface=s0,
            actual_reaching_time=reaching_time,
            theoretical_reaching_time=theoretical_reaching_time,
            reachability_condition_satisfied=reachability_condition_satisfied,
            reaching_rate_violations=reaching_rate_violations,
            finite_time_reachable=reaching_time is not None and reaching_time < float('inf')
        ))

    return ReachabilityValidationResult(
        test_results=reachability_results,
        overall_reachability=all(r.finite_time_reachable for r in reachability_results),
        reachability_percentage=len([r for r in reachability_results if r.finite_time_reachable]) / len(reachability_results) * 100,
        mathematical_interpretation=_interpret_reachability_results(reachability_results)
    )