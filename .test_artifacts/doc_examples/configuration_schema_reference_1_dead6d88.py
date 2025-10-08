# Example from: docs\technical\configuration_schema_reference.md
# Index: 1
# Runnable: False
# Hash: dead6d88

# example-metadata:
# runnable: false

CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
        'gain_count': 6,
        'description': 'Classical sliding mode controller with boundary layer',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'boundary_layer']
    },
    # ... other controllers
}