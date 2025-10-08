# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 4
# Runnable: True
# Hash: 10ef4765

from src.utils.validation.parameter_validators import require_finite

# Initial conditions (can be positive, negative, or zero)
x0 = require_finite(0.0, "initial_position")       # ✅
theta0 = require_finite(-0.1, "initial_angle")     # ✅
velocity = require_finite(1.5, "initial_velocity") # ✅

# Invalid: infinite value
try:
    x = require_finite(float('inf'), "measurement")
except ValueError as e:
    # Error: "measurement must be a finite number; got inf"
    print(e)

# Invalid: NaN value
try:
    x = require_finite(float('nan'), "sensor_reading")
except ValueError as e:
    # Error: "sensor_reading must be a finite number; got nan"
    print(e)