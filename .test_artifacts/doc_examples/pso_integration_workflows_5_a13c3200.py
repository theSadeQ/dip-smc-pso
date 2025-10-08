# Example from: docs\technical\pso_integration_workflows.md
# Index: 5
# Runnable: False
# Hash: a13c3200

# example-metadata:
# runnable: false

# Optimize STA-SMC with Issue #2 considerations
pso_config = PSOFactoryConfig(
    controller_type=ControllerType.STA_SMC,
    population_size=25,    # Larger population for better exploration
    max_iterations=75      # More iterations for convergence
)

pso_factory = EnhancedPSOFactory(pso_config)
result = pso_factory.optimize_controller()

if result['success']:
    # Verify reduced overshoot (Issue #2 resolution)
    performance = result['performance_analysis']
    print(f"Converged: {performance['converged']}")
    print(f"Improvement ratio: {performance['improvement_ratio']:.3f}")

    # Check optimized surface coefficients
    gains = result['best_gains']
    lambda1, lambda2 = gains[4], gains[5]  # λ₁, λ₂ coefficients
    print(f"Optimized surface coefficients: λ₁={lambda1:.3f}, λ₂={lambda2:.3f}")