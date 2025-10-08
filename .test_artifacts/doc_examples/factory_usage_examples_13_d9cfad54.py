# Example from: docs\technical\factory_usage_examples.md
# Index: 13
# Runnable: True
# Hash: d9cfad54

from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig

# Example 1: Invalid surface gains (negative values)
try:
    config = ClassicalSMCConfig(
        gains=[0.0, 5.0, 3.0, 2.0, 10.0, 1.0],  # k1 = 0 violates stability
        max_force=150.0,
        boundary_layer=0.02
    )
except ValueError as e:
    print(f"Configuration validation failed: {e}")
    # Output: "Surface gains [k1, k2, λ1, λ2] must be positive for stability"

# Example 2: Invalid boundary layer (too small)
try:
    config = ClassicalSMCConfig(
        gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
        max_force=150.0,
        boundary_layer=1e-15  # Too small, causes division by zero
    )
except ValueError as e:
    print(f"Configuration validation failed: {e}")
    # Output: "boundary_layer is too small (minimum: 1e-12) which may cause division by zero"

# Example 3: Valid configuration
config = ClassicalSMCConfig(
    gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    max_force=150.0,
    boundary_layer=0.02
)
print("Configuration is valid")