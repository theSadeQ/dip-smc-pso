# Example from: docs\api\factory_system_api_reference.md
# Index: 4
# Runnable: True
# Hash: 861a8aed

# All create the same controller type
controller1 = create_controller('classical_smc', config)
controller2 = create_controller('classic_smc', config)  # Alias
controller3 = create_controller('smc_v1', config)       # Alias