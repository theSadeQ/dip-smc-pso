# Example from: docs\guides\api\optimization.md
# Index: 11
# Runnable: False
# Hash: d781b936

# example-metadata:
# runnable: false

def robust_cost(gains):
    """Optimize for robustness across scenarios."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)

    scenarios = [
        np.array([0, 0, 0.1, 0, 0.15, 0]),   # Nominal
        np.array([0, 0, 0.2, 0, 0.25, 0]),   # Large angles
        np.array([0.1, 0, 0.15, 0, 0.2, 0]), # Cart offset
        np.array([0, 0, -0.1, 0, -0.15, 0]), # Negative angles
    ]

    costs = []
    for ic in scenarios:
        result = runner.run(controller, initial_state=ic)
        costs.append(result['metrics']['ise'])

    # Worst-case optimization
    return max(costs)

    # Or average-case
    # return np.mean(costs)