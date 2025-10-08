# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 16
# Runnable: True
# Hash: b491e7ba

from src.optimization.integration.pso_factory_bridge import (
    EnhancedPSOFactory, PSOFactoryConfig, ControllerType
)

# Configure PSO optimization
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=20,
    max_iterations=50,
    convergence_threshold=1e-6,
    enable_adaptive_bounds=True,
    use_robust_evaluation=True
)

# Create enhanced PSO factory
pso_factory = EnhancedPSOFactory(pso_config, "config.yaml")

# Run optimization with comprehensive monitoring
result = pso_factory.optimize_controller()