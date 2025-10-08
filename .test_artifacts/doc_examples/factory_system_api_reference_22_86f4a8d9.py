# Example from: docs\api\factory_system_api_reference.md
# Index: 22
# Runnable: True
# Hash: 86f4a8d9

'classical_smc': {
    'class': ClassicalSMC,
    'config_class': ClassicalSMCConfig,
    'default_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    'gain_count': 6,
    'description': 'Classical sliding mode controller with boundary layer',
    'supports_dynamics': True,
    'required_params': ['gains', 'max_force', 'boundary_layer']
}