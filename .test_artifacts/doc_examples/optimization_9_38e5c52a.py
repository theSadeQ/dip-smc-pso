# Example from: docs\guides\api\optimization.md
# Index: 9
# Runnable: False
# Hash: 38e5c52a

def constrained_cost(gains):
    """Enforce stability constraints."""
    # Constraint: First gain must be larger than second
    if gains[0] <= gains[1]:
        return float('inf')

    # Constraint: Switching gain must be significant
    if gains[4] < 10.0:
        return float('inf')

    # Evaluate if valid
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    result = runner.run(controller)
    return result['metrics']['ise']