# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 22
# Runnable: True
# Hash: fc786c19

if K <= 0:
    raise ValueError("Switching gain K must be positive")
if kd < 0:
    raise ValueError("Derivative gain kd must be non-negative")