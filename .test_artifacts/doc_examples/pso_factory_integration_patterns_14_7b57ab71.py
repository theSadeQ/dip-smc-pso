# Example from: docs\pso_factory_integration_patterns.md
# Index: 14
# Runnable: False
# Hash: 7b57ab71

# ✅ Good: Validate gains before expensive simulation
def robust_fitness_function(gains):
    if not validate_smc_gains(controller_type, gains):
        return float('inf')  # Early exit for invalid gains

    controller = factory(gains)
    return evaluate_performance(controller)

# ❌ Bad: No validation, let controller creation fail
def fragile_fitness_function(gains):
    controller = factory(gains)  # May fail with cryptic error
    return evaluate_performance(controller)