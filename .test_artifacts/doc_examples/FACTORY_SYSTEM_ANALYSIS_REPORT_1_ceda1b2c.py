# Example from: docs\reports\FACTORY_SYSTEM_ANALYSIS_REPORT.md
# Index: 1
# Runnable: False
# Hash: ceda1b2c

# example-metadata:
# runnable: false

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