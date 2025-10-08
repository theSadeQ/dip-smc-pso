# Example from: docs\api\factory_methods_reference.md
# Index: 25
# Runnable: False
# Hash: 59a072ff

# example-metadata:
# runnable: false

# Validate gains before expensive simulation
def robust_fitness_function(gains):
    if not validate_smc_gains(SMCType.CLASSICAL, gains):
        return float('inf')  # Invalid gains get worst fitness

    controller = create_smc_for_pso(SMCType.CLASSICAL, gains)
    return evaluate_controller_performance(controller)

# Test various gain sets
test_gains = [
    [20, 15, 12, 8, 35, 5],     # Valid
    [20, 15, 12, 8, 35],        # Wrong length
    [20, 15, 12, 8, -35, 5],    # Negative value
    [20, 15, 12, 8, np.inf, 5], # Infinite value
]

for i, gains in enumerate(test_gains):
    valid = validate_smc_gains(SMCType.CLASSICAL, gains)
    print(f"Gains {i+1}: {'Valid' if valid else 'Invalid'}")