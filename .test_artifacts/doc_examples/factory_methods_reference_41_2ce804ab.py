# Example from: docs\api\factory_methods_reference.md
# Index: 41
# Runnable: True
# Hash: 2ce804ab

try:
    controller = create_controller('mpc_controller', config=invalid_config)
except ConfigValueError as e:
    print(f"Configuration error: {e}")
    # Handle invalid configuration