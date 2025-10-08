# Example from: docs\technical\pso_integration_workflows.md
# Index: 8
# Runnable: False
# Hash: 1e3f57bd

# Configure PSO for multi-objective optimization
multi_objective_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=40,              # Larger population for Pareto front
    max_iterations=150,              # Extended search
    convergence_threshold=1e-6,      # High precision
    enable_adaptive_bounds=True,     # Dynamic exploration
    fitness_timeout=20.0            # Longer evaluations
)

pso_factory = EnhancedPSOFactory(multi_objective_config)

# The enhanced fitness function automatically considers:
# - State regulation performance
# - Control effort minimization
# - Control smoothness
# - Stability margins
# - Robustness to disturbances

result = pso_factory.optimize_controller()