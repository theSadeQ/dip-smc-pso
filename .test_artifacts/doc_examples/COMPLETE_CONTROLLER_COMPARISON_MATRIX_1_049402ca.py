# Example from: docs\analysis\COMPLETE_CONTROLLER_COMPARISON_MATRIX.md
# Index: 1
# Runnable: False
# Hash: 049402ca

# example-metadata:
# runnable: false

pso_performance_matrix = {
    'classical_smc': {
        'convergence_quality': 'EXCELLENT',
        'achieved_target': True,
        'computational_cost': 0.365,
        'parameter_space': 6,
        'convergence_rate': 'Fast'
    },
    'adaptive_smc': {
        'convergence_quality': 'STABLE',
        'achieved_target': True,
        'computational_cost': 0.420,
        'parameter_space': 5,
        'convergence_rate': 'Steady'
    },
    'sta_smc': {
        'convergence_quality': 'EXCELLENT',
        'achieved_target': True,
        'computational_cost': 0.134,
        'parameter_space': 6,
        'convergence_rate': 'Very Fast'
    },
    'hybrid_adaptive_sta_smc': {
        'convergence_quality': 'OPTIMAL',
        'achieved_target': True,
        'computational_cost': 0.287,
        'parameter_space': 4,
        'convergence_rate': 'Optimal'
    }
}