# Example from: docs\factory\configuration_reference.md
# Index: 15
# Runnable: True
# Hash: 6b1088d2

# Only add dynamics_model for controllers that support it
if dynamics_model is not None and controller_type in ['classical_smc', 'sta_smc', 'adaptive_smc', 'mpc_controller']:
    config_params['dynamics_model'] = dynamics_model