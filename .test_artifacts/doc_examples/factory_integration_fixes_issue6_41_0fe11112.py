# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 41
# Runnable: True
# Hash: 0fe11112

# New way - comprehensive PSO-factory integration
from src.optimization.integration.pso_factory_bridge import (
    EnhancedPSOFactory, PSOFactoryConfig, ControllerType
)

pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=20,
    max_iterations=50,
    use_robust_evaluation=True
)

pso_factory = EnhancedPSOFactory(pso_config)
result = pso_factory.optimize_controller()

# Result includes:
# - Optimized controller instance
# - Convergence analysis
# - Performance validation
# - Comprehensive diagnostics