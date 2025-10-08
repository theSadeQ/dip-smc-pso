# Example from: docs\factory\parameter_interface_specification.md
# Index: 2
# Runnable: False
# Hash: c0bfa37b

# Parameter Structure: [k1, k2, λ1, λ2, K, kd]
ClassicalSMCParameters = {
    'gains': {
        'count': 6,
        'names': ['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd'],
        'bounds': [(0.1, 50.0), (0.1, 50.0), (0.1, 20.0), (0.1, 20.0), (1.0, 200.0), (0.0, 50.0)],
        'physical_meaning': {
            'k1': 'First pendulum surface gain',
            'k2': 'Second pendulum surface gain',
            'lambda1': 'First pendulum sliding coefficient',
            'lambda2': 'Second pendulum sliding coefficient',
            'K': 'Switching control gain',
            'kd': 'Damping gain for chattering reduction'
        }
    },
    'required_params': ['boundary_layer'],
    'optional_params': ['switch_method', 'damping_gain'],
    'stability_constraints': [
        'All gains must be positive',
        'k1, k2 determine convergence rate',
        'λ1, λ2 affect sliding surface slope',
        'K must overcome system uncertainties',
        'boundary_layer > 0 for chattering reduction'
    ]
}