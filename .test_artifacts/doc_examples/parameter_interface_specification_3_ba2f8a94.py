# Example from: docs\factory\parameter_interface_specification.md
# Index: 3
# Runnable: False
# Hash: ba2f8a94

# example-metadata:
# runnable: false

# Parameter Structure: [k1, k2, λ1, λ2, γ]
AdaptiveSMCParameters = {
    'gains': {
        'count': 5,
        'names': ['k1', 'k2', 'lambda1', 'lambda2', 'gamma'],
        'bounds': [(0.1, 50.0), (0.1, 50.0), (0.1, 25.0), (0.1, 25.0), (0.01, 10.0)],
        'physical_meaning': {
            'k1': 'First pendulum surface gain',
            'k2': 'Second pendulum surface gain',
            'lambda1': 'First pendulum sliding coefficient',
            'lambda2': 'Second pendulum sliding coefficient',
            'gamma': 'Adaptation rate for parameter estimation (gains[4])'
        }
    },
    'gamma_extraction': {
        'method': 'array_indexing',
        'index': 4,
        'validation': 'gamma = gains[4], must be in (0.01, 10.0)',
        'deprecation_note': 'Separate gamma parameter deprecated in v2.0.0'
    },
    'adaptation_params': {
        'leak_rate': 0.01,
        'adapt_rate_limit': 10.0,
        'K_min': 0.1,
        'K_max': 100.0,
        'K_init': 10.0,
        'alpha': 0.5,
        'dead_zone': 0.05
    }
}