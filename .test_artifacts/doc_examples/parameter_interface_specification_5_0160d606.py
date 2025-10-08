# Example from: docs\factory\parameter_interface_specification.md
# Index: 5
# Runnable: False
# Hash: 0160d606

# example-metadata:
# runnable: false

# Parameter Structure: [k1, k2, λ1, λ2] (surface gains only)
HybridSMCParameters = {
    'gains': {
        'count': 4,
        'names': ['k1', 'k2', 'lambda1', 'lambda2'],
        'bounds': [(0.1, 50.0), (0.1, 50.0), (0.1, 20.0), (0.1, 20.0)],
        'physical_meaning': {
            'k1': 'First pendulum surface gain',
            'k2': 'Second pendulum surface gain',
            'lambda1': 'First pendulum sliding coefficient',
            'lambda2': 'Second pendulum sliding coefficient'
        }
    },
    'sub_configurations': {
        'classical_config': 'Full ClassicalSMCConfig instance',
        'adaptive_config': 'Full AdaptiveSMCConfig instance',
        'hybrid_mode': 'HybridMode.CLASSICAL_ADAPTIVE enum'
    },
    'initialization_gains': {
        'k1_init': 5.0,
        'k2_init': 3.0,
        'gamma1': 0.5,
        'gamma2': 0.3
    }
}