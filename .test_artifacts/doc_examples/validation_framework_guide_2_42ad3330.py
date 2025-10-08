# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 2
# Runnable: True
# Hash: 42ad3330

from src.utils.validation.parameter_validators import require_positive

# Control gains must be positive
k_p = require_positive(10.0, "proportional_gain")  # ✅ Returns 10.0

# Mass parameters must be positive
mass = require_positive(1.5, "cart_mass")  # ✅ Returns 1.5

# Friction can be zero (but not negative)
friction = require_positive(0.0, "friction_coefficient", allow_zero=True)  # ✅ Returns 0.0

# Invalid: negative gain
try:
    k_p = require_positive(-5.0, "proportional_gain")
except ValueError as e:
    # Error: "proportional_gain must be > 0; got -5.0"
    print(e)