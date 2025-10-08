# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 1
# Runnable: False
# Hash: beca8043

CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],  # 6 gains
        'gain_count': 6,
        'supports_dynamics': True
    },
    'sta_smc': {
        'class': ModularSuperTwistingSMC,
        'config_class': STASMCConfig,
        'default_gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],  # 6 gains with K1 > K2
        'gain_count': 6,
        'supports_dynamics': True
    },
    'adaptive_smc': {
        'class': ModularAdaptiveSMC,
        'config_class': AdaptiveSMCConfig,
        'default_gains': [25.0, 18.0, 15.0, 10.0, 4.0],       # 5 gains
        'gain_count': 5,
        'supports_dynamics': True
    },
    'hybrid_adaptive_sta_smc': {
        'class': ModularHybridSMC,
        'config_class': HybridAdaptiveSTASMCConfig,
        'default_gains': [18.0, 12.0, 10.0, 8.0],             # 4 surface gains
        'gain_count': 4,
        'supports_dynamics': False  # Uses sub-controllers
    }
}