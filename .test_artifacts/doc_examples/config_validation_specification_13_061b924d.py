# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 13
# Runnable: True
# Hash: 061b924d

if self.regularization <= 0:
    raise ValueError("regularization must be positive")