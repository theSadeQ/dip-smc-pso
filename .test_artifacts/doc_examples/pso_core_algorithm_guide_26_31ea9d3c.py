# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 26
# Runnable: False
# Hash: 31ea9d3c

# Production-ready PSO configuration
pso_config = {
    'population_size': 30,
    'max_iterations': 100,
    'inertia_weight': 0.7298,
    'cognitive_weight': 2.05,
    'social_weight': 2.05,
    'adaptive_weights': True,
    'velocity_clamping': True,
    'tolerance': 1e-6,
}