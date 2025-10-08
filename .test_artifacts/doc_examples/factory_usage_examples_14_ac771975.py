# Example from: docs\technical\factory_usage_examples.md
# Index: 14
# Runnable: True
# Hash: ac771975

from src.optimization.integration.pso_factory_bridge import EnhancedPSOFactory, PSOFactoryConfig, ControllerType

# Configure PSO with robust evaluation
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    use_robust_evaluation=True,  # Enable automatic error recovery
    fitness_timeout=10.0         # Timeout protection
)

pso_factory = EnhancedPSOFactory(pso_config)

# The enhanced factory automatically handles:
# - Controller creation failures
# - Simulation instabilities
# - Matrix singularities
# - Timeout conditions
# - Invalid parameter combinations

result = pso_factory.optimize_controller()

# Check optimization statistics
stats = pso_factory.validation_stats
print(f"Total fitness evaluations: {stats['fitness_evaluations']}")
print(f"Failed evaluations: {stats['failed_evaluations']}")
print(f"Parameter violations: {stats['parameter_violations']}")

# Calculate success rate
success_rate = 1.0 - (stats['failed_evaluations'] / max(stats['fitness_evaluations'], 1))
print(f"Evaluation success rate: {success_rate:.1%}")