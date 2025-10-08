# Example from: docs\GitHub_Issue_4_PSO_Integration_Resolution_Report.md
# Index: 6
# Runnable: False
# Hash: 3a00fa01

# example-metadata:
# runnable: false

def cost_function(gains: np.ndarray) -> float:
    """
    Comprehensive cost function for SMC parameter optimization.

    Cost Components:
    1. Tracking performance (ISE, ITAE)
    2. Control effort minimization
    3. Stability margins
    4. Constraint violations
    5. Issue #2 overshoot penalties (STA-SMC)
    """
    try:
        # Create controller with PSO gains
        controller = create_smc_for_pso(controller_type, gains)

        # Simulate across multiple scenarios
        total_cost = 0.0
        for scenario in test_scenarios:
            sim_result = simulate_scenario(controller, scenario)

            # Performance metrics
            tracking_cost = compute_tracking_cost(sim_result)
            control_cost = compute_control_effort(sim_result)
            stability_cost = compute_stability_margin(sim_result)

            # Issue #2 specific penalty for STA-SMC
            if controller_type == 'sta_smc':
                overshoot_penalty = compute_overshoot_penalty(sim_result)
                total_cost += overshoot_penalty

            total_cost += tracking_cost + 0.1 * control_cost + 0.05 * stability_cost

        return total_cost

    except Exception:
        return 1e6  # High penalty for invalid parameters