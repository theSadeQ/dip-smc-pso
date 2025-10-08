# Example from: docs\api\factory_methods_reference.md
# Index: 13
# Runnable: False
# Hash: 409104c0

# example-metadata:
# runnable: false

# Get default gains for different controllers
classical_gains = get_default_gains('classical_smc')
print(f"Classical SMC defaults: {classical_gains}")
# Output: [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]

adaptive_gains = get_default_gains('adaptive_smc')
print(f"Adaptive SMC defaults: {adaptive_gains}")
# Output: [25.0, 18.0, 15.0, 10.0, 4.0]

# Use as starting point for optimization
optimized_gains = optimize_controller_gains(
    controller_type='classical_smc',
    initial_gains=get_default_gains('classical_smc')
)