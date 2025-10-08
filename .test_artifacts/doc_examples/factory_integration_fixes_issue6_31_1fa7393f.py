# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 31
# Runnable: False
# Hash: 1fa7393f

# example-metadata:
# runnable: false

# Use enhanced PSO factory with robust evaluation
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    use_robust_evaluation=True,  # Enables error recovery
    fitness_timeout=15.0  # Timeout for stuck evaluations
)

pso_factory = EnhancedPSOFactory(pso_config)

# The enhanced factory automatically handles:
# - Matrix singularities in dynamics
# - Controller computation failures
# - Unstable simulation trajectories
# - Timeout protection