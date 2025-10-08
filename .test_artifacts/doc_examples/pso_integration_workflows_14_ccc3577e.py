# Example from: docs\technical\pso_integration_workflows.md
# Index: 14
# Runnable: False
# Hash: ccc3577e

# example-metadata:
# runnable: false

from src.optimization.integration.pso_factory_bridge import EnhancedPSOFactory

# Create PSO factory with monitoring
pso_factory = EnhancedPSOFactory(pso_config)

# Start optimization
print("Starting optimization with real-time monitoring...")
result = pso_factory.optimize_controller()

# Access monitoring statistics
stats = pso_factory.validation_stats
print(f"\nOptimization Statistics:")
print(f"  Total fitness evaluations: {stats['fitness_evaluations']}")
print(f"  Failed evaluations: {stats['failed_evaluations']}")
print(f"  Parameter violations: {stats['parameter_violations']}")
print(f"  Convergence checks: {stats['convergence_checks']}")

# Calculate success metrics
success_rate = 1.0 - (stats['failed_evaluations'] / max(stats['fitness_evaluations'], 1))
print(f"  Evaluation success rate: {success_rate:.1%}")