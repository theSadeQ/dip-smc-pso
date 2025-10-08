# Example from: docs\technical\controller_factory_integration.md
# Index: 2
# Runnable: False
# Hash: 6080d6d2

CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [5.0, 5.0, 5.0, 0.5, 0.5, 0.5]
    },
    'sta_smc': {
        'class': ModularSuperTwistingSMC,
        'config_class': STASMCConfig,
        'default_gains': [5.0, 3.0, 4.0, 4.0, 0.4, 0.4]
    },
    'adaptive_smc': {
        'class': ModularAdaptiveSMC,
        'config_class': AdaptiveSMCConfig,
        'default_gains': [10.0, 8.0, 5.0, 4.0, 1.0]
    },
    'hybrid_adaptive_sta_smc': {
        'class': ModularHybridSMC,
        'config_class': HybridAdaptiveSTASMCConfig,
        'default_gains': [5.0, 5.0, 5.0, 0.5]
    }
}