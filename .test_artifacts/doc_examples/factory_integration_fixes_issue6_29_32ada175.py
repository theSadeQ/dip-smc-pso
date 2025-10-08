# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 29
# Runnable: False
# Hash: 32ada175

# 1. Check parameter bounds
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
print(f"Bounds: {bounds}")

# 2. Adjust PSO configuration
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=30,  # Increase population
    max_iterations=100,  # More iterations
    convergence_threshold=1e-5,  # Stricter convergence
    fitness_timeout=20.0  # Longer evaluation time
)

# 3. Enable robust evaluation
pso_config.use_robust_evaluation = True

# 4. Check diagnostics
diagnostics = pso_factory.get_optimization_diagnostics()
print(f"Failed evaluations: {diagnostics['validation_statistics']['failed_evaluations']}")
print(f"Parameter violations: {diagnostics['validation_statistics']['parameter_violations']}")