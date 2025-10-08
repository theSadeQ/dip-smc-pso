# Example from: docs\api\factory_methods_reference.md
# Index: 9
# Runnable: True
# Hash: be3c8a9d

available = list_available_controllers()
print("Available controllers:", available)
# Output: ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']
# Note: 'mpc_controller' only included if optional dependencies available