# Example from: docs\technical\pso_integration_workflows.md
# Index: 9
# Runnable: True
# Hash: acb4f772

from src.controllers.factory import get_gain_bounds_for_pso, SMCType

# Get controller-specific bounds
smc_type = SMCType.CLASSICAL
bounds = get_gain_bounds_for_pso(smc_type)
lower_bounds, upper_bounds = bounds

print(f"Classical SMC optimization bounds:")
print(f"  Lower: {lower_bounds}")
print(f"  Upper: {upper_bounds}")

# Configure PSO with custom bounds
constrained_config = PSOFactoryConfig(
    controller_type=ControllerType.CLASSICAL_SMC,
    population_size=25,
    max_iterations=60,
    enable_adaptive_bounds=False  # Use fixed bounds
)

pso_factory = EnhancedPSOFactory(constrained_config)

# Factory automatically applies controller-specific bounds:
# Classical SMC: [k1, k2, λ1, λ2, K, kd] bounds
# - Position gains: [1.0, 30.0]
# - Surface coefficients: [1.0, 20.0]
# - Switching gain: [5.0, 50.0]
# - Derivative gain: [0.1, 10.0]

result = pso_factory.optimize_controller()