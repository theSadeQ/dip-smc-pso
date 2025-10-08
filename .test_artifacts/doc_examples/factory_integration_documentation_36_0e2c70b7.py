# Example from: docs\factory_integration_documentation.md
# Index: 36
# Runnable: False
# Hash: 0e2c70b7

# example-metadata:
# runnable: false

# Memory-efficient patterns:

# 1. Reuse factory functions
factory = create_pso_controller_factory(SMCType.CLASSICAL)
# Use factory many times without recreating

# 2. Use minimal configurations when possible
controller = create_controller('classical_smc', gains=simple_gains)
# Avoid complex config objects for simple use cases

# 3. Batch operations
controllers = create_all_smc_controllers(gains_dict)
# More efficient than individual creation