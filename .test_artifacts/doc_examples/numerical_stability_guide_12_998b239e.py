# Example from: docs\numerical_stability_guide.md
# Index: 12
# Runnable: True
# Hash: 998b239e

# NEW (v1.2.0+)
controller_config = {
    'regularization_alpha': 1e-4,          # Base scaling factor
    'min_regularization': 1e-10,           # Safety floor
    'max_condition_number': 1e14,          # Condition threshold
    'use_adaptive_regularization': True    # Enable adaptive mode
}