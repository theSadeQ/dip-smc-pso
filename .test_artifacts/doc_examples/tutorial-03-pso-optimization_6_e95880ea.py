# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 6
# Runnable: False
# Hash: e95880ea

def custom_cost_function(metrics: dict, config: dict) -> float:
    """
    Custom cost emphasizing settling time with hard constraints.

    Returns float('inf') if constraints violated.
    """
    # Hard constraints (return infinite cost if violated)
    if metrics['overshoot'] > 10.0:  # Max 10% overshoot
        return float('inf')

    if metrics['max_control'] > 100.0:  # Actuator limit
        return float('inf')

    # Primary objective: settling time
    cost = 0.6 * metrics['settling_time']

    # Secondary objectives
    cost += 0.2 * metrics['ise']
    cost += 0.1 * metrics['control_effort'] / 100.0  # Normalize
    cost += 0.1 * metrics['overshoot'] / 10.0        # Normalize

    return cost