# Example from: docs\technical\factory_usage_examples.md
# Index: 2
# Runnable: True
# Hash: 78381ca4

# Multiple ways to create the same controller
controllers = [
    create_controller('classical_smc', gains),
    create_controller('classic_smc', gains),       # Alias
    create_controller('smc_classical', gains),     # Alias
    create_controller('smc_v1', gains),           # Alias
]

# All create identical Classical SMC controllers
assert all(type(c) == type(controllers[0]) for c in controllers)