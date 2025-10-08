# Example from: docs\api\factory_system_api_reference.md
# Index: 53
# Runnable: True
# Hash: 05caa117

try:
    controller = create_controller('nonexistent_controller')
except ValueError as e:
    print(e)
    # Output: "Unknown controller type 'nonexistent_controller'.
    #          Available: ['adaptive_smc', 'classical_smc', 'hybrid_adaptive_sta_smc',
    #                      'mpc_controller', 'sta_smc']"