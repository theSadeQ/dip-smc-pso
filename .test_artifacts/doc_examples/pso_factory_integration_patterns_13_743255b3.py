# Example from: docs\pso_factory_integration_patterns.md
# Index: 13
# Runnable: True
# Hash: 743255b3

# ✅ Good: Create factory once, use many times
factory = create_pso_controller_factory(SMCType.CLASSICAL)

def fitness_function(gains):
    controller = factory(gains)  # Fast operation
    return evaluate_performance(controller)

# ❌ Bad: Recreate factory every time
def fitness_function(gains):
    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)  # Slow operation
    return evaluate_performance(controller)