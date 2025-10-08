# Example from: docs\guides\api\optimization.md
# Index: 10
# Runnable: False
# Hash: 8d4b11be

# example-metadata:
# runnable: false

def penalty_based_cost(gains):
    """Use penalties for soft constraints."""
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)

    cost = result['metrics']['ise']

    # Penalty for excessive control saturation
    if result['metrics']['saturation_percentage'] > 20.0:
        penalty = result['metrics']['saturation_percentage'] * 0.5
        cost += penalty

    # Penalty for overshoot
    max_theta = max(result['metrics']['max_theta1'], result['metrics']['max_theta2'])
    if max_theta > 0.3:  # 17 degrees
        cost += (max_theta - 0.3) * 100

    return cost