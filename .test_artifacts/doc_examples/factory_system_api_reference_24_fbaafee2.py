# Example from: docs\api\factory_system_api_reference.md
# Index: 24
# Runnable: True
# Hash: fbaafee2

'adaptive_smc': {
    'class': AdaptiveSMC,
    'config_class': AdaptiveSMCConfig,
    'default_gains': [25.0, 18.0, 15.0, 10.0, 4.0],
    'gain_count': 5,
    'description': 'Adaptive sliding mode controller with parameter estimation',
    'supports_dynamics': True,
    'required_params': ['gains', 'max_force', 'dt']
}