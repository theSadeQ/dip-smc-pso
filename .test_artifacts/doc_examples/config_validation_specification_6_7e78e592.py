# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 6
# Runnable: True
# Hash: 7e78e592

if self.max_force <= 0:
    raise ValueError("max_force must be positive")