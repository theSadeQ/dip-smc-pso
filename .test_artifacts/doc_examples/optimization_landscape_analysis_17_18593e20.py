# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 17
# Runnable: True
# Hash: 18593e20

recommended_pso_config = {
    'n_particles': 30,          # Balanced swarm size
    'max_iters': 100,           # Sufficient for convergence
    'inertia': [0.9, 0.4],      # Linear decrease
    'c1': 2.05,                 # Standard cognitive
    'c2': 2.05,                 # Standard social
    'boundary_handling': 'absorbing',
    'velocity_clamping': 0.2,
}