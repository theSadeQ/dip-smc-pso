# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 10
# Runnable: True
# Hash: 6972fa7e

if self.boundary_layer_slope < 0:
    raise ValueError("boundary_layer_slope must be non-negative")