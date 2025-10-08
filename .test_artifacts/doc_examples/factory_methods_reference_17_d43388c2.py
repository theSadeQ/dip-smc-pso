# Example from: docs\api\factory_methods_reference.md
# Index: 17
# Runnable: False
# Hash: d43388c2

# Create factory once (expensive operation)
factory = create_pso_controller_factory(
    SMCType.CLASSICAL,
    plant_config=config.physics,
    max_force=150.0
)

# Check factory attributes
print(f"Required gains: {factory.n_gains}")
print(f"Controller type: {factory.controller_type}")
print(f"Max force: {factory.max_force}")

# Use factory many times (fast operation)
def pso_fitness_function(gains):
    controller = factory(gains)  # Fast!
    return evaluate_controller_performance(controller)

# PSO optimization
tuner = PSOTuner(
    controller_factory=pso_fitness_function,
    config=config
)
best_gains, best_fitness = tuner.optimize()