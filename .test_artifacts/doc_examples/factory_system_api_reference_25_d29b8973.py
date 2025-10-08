# Example from: docs\api\factory_system_api_reference.md
# Index: 25
# Runnable: True
# Hash: d29b8973

'hybrid_adaptive_sta_smc': {
    'class': ModularHybridSMC,
    'config_class': HybridAdaptiveSTASMCConfig,
    'default_gains': [18.0, 12.0, 10.0, 8.0],
    'gain_count': 4,
    'description': 'Hybrid adaptive super-twisting sliding mode controller',
    'supports_dynamics': False,  # Uses sub-controllers
    'required_params': ['classical_config', 'adaptive_config', 'hybrid_mode']
}