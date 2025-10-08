# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 21
# Runnable: True
# Hash: 413bc873

pso_exploitative = {
    'population_size': 20,     # Small swarm
    'inertia_weight': 0.4,     # Low exploration
    'cognitive_weight': 1.5,   # Weak personal
    'social_weight': 2.5,      # Strong social
    'max_iterations': 50,
}