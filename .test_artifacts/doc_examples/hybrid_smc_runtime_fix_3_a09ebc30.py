# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 3
# Runnable: True
# Hash: a09ebc30

# Error cascade analysis
error_propagation = {
    'compute_control_returns_none': 'Primary failure',
    'simulation_engine_confusion': 'Type handling error',
    'factory_error_handling': 'Exception caught and masked',
    'pso_fitness_receives_string': 'Error message interpreted as fitness',
    'pso_perfect_cost': 'String converted to 0.0 fitness value',
    'false_optimization_success': 'Misleading PSO results'
}