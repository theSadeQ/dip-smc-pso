# Example from: docs\factory_integration_documentation.md
# Index: 37
# Runnable: False
# Hash: 2a97f6bb

# example-metadata:
# runnable: false

# Thread-safe patterns:

# 1. Pre-create factories for concurrent use
factories = {
    SMCType.CLASSICAL: create_pso_controller_factory(SMCType.CLASSICAL),
    SMCType.ADAPTIVE: create_pso_controller_factory(SMCType.ADAPTIVE),
}

# 2. Use factories in parallel PSO
def parallel_fitness_evaluation(gains_batch):
    factory = factories[controller_type]
    return [evaluate_controller(factory(gains)) for gains in gains_batch]