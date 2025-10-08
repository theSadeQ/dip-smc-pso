# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 16
# Runnable: False
# Hash: 4f2a7cae

# example-metadata:
# runnable: false

# Custom PSO configuration for difficult landscape
pso_advanced = ParticleSwarmOptimizer(
    parameter_space=param_space,
    population_size=50,              # Larger swarm for multimodality
    max_iterations=200,              # More iterations
    inertia_weight=0.9,              # High initial exploration
    cognitive_weight=2.5,            # Strong personal attraction
    social_weight=1.5,               # Moderate social attraction
    adaptive_weights=True,
    velocity_clamping=True,
    tolerance=1e-6,                  # Tight convergence
)

# Custom adaptive strategy
pso_advanced.initial_inertia = 0.9
pso_advanced.final_inertia = 0.3
pso_advanced.initial_c1 = 2.5
pso_advanced.final_c1 = 0.5
pso_advanced.initial_c2 = 1.5
pso_advanced.final_c2 = 3.0

result = pso_advanced.optimize(fitness_function)