# Example from: docs\factory\configuration_reference.md
# Index: 2
# Runnable: False
# Hash: 907e88a7

CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [8.0, 6.0, 4.0, 3.0, 15.0, 2.0],  # [k1, k2, λ1, λ2, K, kd]
        'gain_count': 6,
        'description': 'Classical sliding mode controller with boundary layer',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'boundary_layer']
    }
}