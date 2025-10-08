# Example from: docs\analysis\COMPLETE_CONTROLLER_COMPARISON_MATRIX.md
# Index: 3
# Runnable: False
# Hash: 71992445

def select_smc_controller(requirements):
    """Decision tree for SMC controller selection."""

    if requirements.get('parameter_uncertainty') == 'high':
        if requirements.get('convergence_time') == 'finite':
            return 'hybrid_adaptive_sta_smc'  # Best of both worlds
        else:
            return 'adaptive_smc'  # Parameter adaptation focus

    elif requirements.get('convergence_time') == 'finite':
        if requirements.get('chattering_tolerance') == 'low':
            return 'sta_smc'  # Finite-time + smooth control
        else:
            return 'classical_smc'  # Fast and simple

    elif requirements.get('computational_resources') == 'limited':
        return 'classical_smc'  # Lowest computational cost

    elif requirements.get('performance_priority') == 'maximum':
        return 'hybrid_adaptive_sta_smc'  # Best overall performance

    else:
        return 'classical_smc'  # Default choice for general use