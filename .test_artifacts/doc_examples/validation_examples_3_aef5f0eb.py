# Example from: docs\validation\validation_examples.md
# Index: 3
# Runnable: True
# Hash: aef5f0eb

# Conservative (±20% uncertainty)
parameter_distributions = {
    'mass': {'type': 'uniform', 'low': 0.8, 'high': 1.2},
    'length': {'type': 'uniform', 'low': 0.8, 'high': 1.2},
    'friction': {'type': 'uniform', 'low': 0.0, 'high': 0.2}
}