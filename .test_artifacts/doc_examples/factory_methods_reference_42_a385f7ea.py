# Example from: docs\api\factory_methods_reference.md
# Index: 42
# Runnable: False
# Hash: a385f7ea

# example-metadata:
# runnable: false

# Unknown controller type
try:
    controller = create_controller('invalid_controller')
except ValueError as e:
    print(f"Error: {e}")
    # Output: Unknown controller type 'invalid_controller'. Available: [...]

# Invalid gain count
try:
    controller = create_controller('classical_smc', gains=[1, 2, 3])  # Need 6 gains
except ValueError as e:
    print(f"Error: {e}")
    # Output: Controller 'classical_smc' requires 6 gains, got 3