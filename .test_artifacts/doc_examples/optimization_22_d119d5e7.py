# Example from: docs\guides\api\optimization.md
# Index: 22
# Runnable: False
# Hash: d119d5e7

# example-metadata:
# runnable: false

# Define robust cost function
def robust_cost(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    worst_case = 0.0

    for theta_scale in [0.5, 1.0, 1.5, 2.0]:
        ic = np.array([0, 0, 0.1*theta_scale, 0, 0.15*theta_scale, 0])
        result = runner.run(controller, initial_state=ic)
        worst_case = max(worst_case, result['metrics']['ise'])

    return worst_case

# Optimize for worst-case performance
tuner = PSOTuner(SMCType.CLASSICAL, bounds, cost_function=robust_cost)
robust_gains, _ = tuner.optimize()