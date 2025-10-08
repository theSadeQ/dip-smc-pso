# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 2
# Runnable: True
# Hash: dc037c82

if self.dt <= 0:
    raise ValueError("dt must be positive")