# Example from: docs\api\optimization_module_api_reference.md
# Index: 7
# Runnable: True
# Hash: 9da14f94

# Run with custom PSO parameters
result = tuner.optimise(
    iters_override=200,                    # More iterations
    n_particles_override=50,               # Larger swarm
    options_override={'w': 0.5, 'c1': 2.0, 'c2': 2.0}  # Different hyperparameters
)