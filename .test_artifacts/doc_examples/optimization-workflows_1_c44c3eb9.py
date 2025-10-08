# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 1
# Runnable: False
# Hash: c44c3eb9

def minimal_settling_time_cost(metrics, config):
    """
    Custom cost emphasizing fast settling.

    Hard constraints:
    - Overshoot < 10%
    - Peak control < max_force

    Soft objective:
    - Minimize settling time
    """
    # Hard constraints (return infinite cost if violated)
    if metrics['overshoot'] > 10.0:
        return float('inf')  # Infeasible

    if metrics.get('max_control', 0) > config.get('max_force', 100.0):
        return float('inf')  # Actuator limit violated

    # Primary objective: settling time
    cost = 0.7 * metrics['settling_time']

    # Secondary objectives
    cost += 0.2 * metrics['ise']
    cost += 0.1 * metrics['control_effort'] / 100.0  # Normalize

    return cost