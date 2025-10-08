# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 20
# Runnable: True
# Hash: 2e4dd971

pso_explorative = {
    'population_size': 50,     # Larger swarm
    'inertia_weight': 0.9,     # High exploration
    'cognitive_weight': 2.5,   # Strong personal
    'social_weight': 1.5,      # Weak social
    'max_iterations': 150,
}