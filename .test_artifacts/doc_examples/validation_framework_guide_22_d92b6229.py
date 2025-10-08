# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 22
# Runnable: True
# Hash: d92b6229

# Use descriptive names matching mathematical notation
k_p = require_positive(10.0, "proportional_gain")      # Not "k", "param1"
lambda_1 = require_positive(5.0, "surface_gain_joint1") # Not "l1", "gain"
theta_0 = require_finite(0.1, "initial_angle_rad")      # Include units