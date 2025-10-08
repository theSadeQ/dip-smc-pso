# Example from: docs\api\factory_reference.md
# Index: 4
# Runnable: False
# Hash: f0ece82d

CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'gain_count': 6,
        'description': 'Classical sliding mode controller with boundary layer',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'boundary_layer']
    },
    # ... additional controllers
}