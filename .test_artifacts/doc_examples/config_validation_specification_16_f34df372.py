# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 16
# Runnable: True
# Hash: f34df372

if self.controllability_threshold is not None and self.controllability_threshold <= 0:
    raise ValueError("controllability_threshold must be positive when specified")