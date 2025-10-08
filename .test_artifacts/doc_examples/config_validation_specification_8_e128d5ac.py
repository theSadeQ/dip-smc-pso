# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 8
# Runnable: True
# Hash: e128d5ac

if self.boundary_layer <= 0:
    raise ValueError("boundary_layer must be positive")