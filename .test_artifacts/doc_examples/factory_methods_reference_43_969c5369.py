# Example from: docs\api\factory_methods_reference.md
# Index: 43
# Runnable: False
# Hash: 969c5369

# example-metadata:
# runnable: false

# MPC without optional dependencies
try:
    controller = create_controller('mpc_controller')
except ImportError as e:
    print(f"Import error: {e}")
    # Output: MPC controller missing optional dependency. Available controllers: [...]