# Example from: docs\api\factory_system_api_reference.md
# Index: 23
# Runnable: True
# Hash: fbd3d29d

'sta_smc': {
    'class': SuperTwistingSMC,
    'config_class': STASMCConfig,
    'default_gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
    'gain_count': 6,
    'description': 'Super-twisting sliding mode controller',
    'supports_dynamics': True,
    'required_params': ['gains', 'max_force', 'dt']
}