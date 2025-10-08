# Example from: docs\factory\parameter_interface_specification.md
# Index: 4
# Runnable: False
# Hash: 67f48f0e

# Parameter Structure: [K1, K2, k1, k2, λ1, λ2]
SuperTwistingSMCParameters = {
    'gains': {
        'count': 6,
        'names': ['K1', 'K2', 'k1', 'k2', 'lambda1', 'lambda2'],
        'bounds': [(1.0, 100.0), (1.0, 100.0), (0.1, 50.0), (0.1, 50.0), (0.1, 20.0), (0.1, 20.0)],
        'physical_meaning': {
            'K1': 'First-order sliding mode gain',
            'K2': 'Second-order sliding mode gain',
            'k1': 'First pendulum surface gain',
            'k2': 'Second pendulum surface gain',
            'lambda1': 'First pendulum sliding coefficient',
            'lambda2': 'Second pendulum sliding coefficient'
        }
    },
    'sta_specific_params': {
        'power_exponent': 0.5,
        'regularization': 1e-6,
        'switch_method': 'tanh',
        'damping_gain': 0.0
    },
    'convergence_properties': {
        'finite_time_convergence': True,
        'chattering_reduction': 'Built-in via continuous STA',
        'robustness': 'High against matched uncertainties'
    }
}