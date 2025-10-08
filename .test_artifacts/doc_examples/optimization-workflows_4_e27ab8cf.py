# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 4
# Runnable: False
# Hash: e27ab8cf

def constrained_cost(metrics, config):
    """
    Cost function with strict constraints.
    """
    # Constraint 1: Settling time < 5 seconds
    if metrics['settling_time'] > 5.0:
        penalty = 1000 * (metrics['settling_time'] - 5.0)
        return penalty  # Heavy penalty

    # Constraint 2: Overshoot < 5%
    if metrics['overshoot'] > 5.0:
        penalty = 1000 * (metrics['overshoot'] - 5.0)
        return penalty

    # Constraint 3: Control effort < 200
    if metrics['control_effort'] > 200.0:
        penalty = 1000 * (metrics['control_effort'] - 200.0)
        return penalty

    # All constraints satisfied, minimize ISE
    return metrics['ise']