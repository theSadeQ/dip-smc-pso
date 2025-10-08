# Example from: docs\controllers\factory_system_guide.md
# Index: 2
# Runnable: False
# Hash: 91be223e

# example-metadata:
# runnable: false

CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'gain_count': 6,
        'description': 'Classical sliding mode controller with boundary layer',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'boundary_layer']
    },
    'sta_smc': {
        'class': SuperTwistingSMC,
        'config_class': STASMCConfig,
        'default_gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
        'gain_count': 6,
        # ...
    },
    # ... additional controllers
}