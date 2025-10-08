# Example from: docs\technical\factory_usage_examples.md
# Index: 19
# Runnable: True
# Hash: 536fbfa3

from src.optimization.integration.pso_factory_bridge import EnhancedPSOFactory, PSOFactoryConfig, ControllerType

# Configure PSO for memory efficiency
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=15,        # Smaller population for memory efficiency
    max_iterations=30,         # Fewer iterations for speed
    convergence_threshold=1e-4, # Slightly relaxed convergence
    enable_adaptive_bounds=False, # Disable adaptive bounds for simplicity
    fitness_timeout=5.0        # Shorter timeout for speed
)

pso_factory = EnhancedPSOFactory(pso_config)

# Run efficient optimization
import time
start_time = time.time()
result = pso_factory.optimize_controller()
optimization_time = time.time() - start_time

print(f"Optimization completed in {optimization_time:.2f} seconds")
print(f"Memory-efficient result: cost = {result['best_cost']:.6f}")