# Example from: docs\technical\pso_integration_workflows.md
# Index: 10
# Runnable: False
# Hash: 926b1228

# example-metadata:
# runnable: false

# PSO with adaptive parameters
adaptive_config = PSOFactoryConfig(
    controller_type=ControllerType.STA_SMC,
    population_size=20,
    max_iterations=80,
    convergence_threshold=1e-5,
    max_stagnation_iterations=12,
    enable_adaptive_bounds=True,     # Key feature
    enable_gradient_guidance=False,   # Pure PSO
    use_robust_evaluation=True
)

pso_factory = EnhancedPSOFactory(adaptive_config)

# Adaptive bounds automatically:
# - Narrow search ranges during convergence
# - Expand ranges during stagnation
# - Adjust based on swarm diversity

result = pso_factory.optimize_controller()

# Monitor adaptive behavior
diagnostics = pso_factory.get_optimization_diagnostics()
print(f"Adaptive bounds enabled: {diagnostics['configuration']['enable_adaptive_bounds']}")