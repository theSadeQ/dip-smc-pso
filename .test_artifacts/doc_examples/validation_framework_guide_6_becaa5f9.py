# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 6
# Runnable: True
# Hash: becaa5f9

from src.utils.validation.range_validators import require_in_range

# Adaptation rates (bounded for stability)
alpha = require_in_range(0.01, "adaptation_rate", minimum=1e-6, maximum=1.0)  # ✅

# Normalized values
confidence = require_in_range(0.85, "confidence", minimum=0.0, maximum=1.0)  # ✅

# Control saturation limits
u_max = require_in_range(50.0, "max_control", minimum=10.0, maximum=200.0)  # ✅

# Exclusive bounds (value must be strictly inside interval)
threshold = require_in_range(
    0.5, "threshold",
    minimum=0.0, maximum=1.0,
    allow_equal=False  # 0 < threshold < 1
)  # ✅

# Invalid: below minimum
try:
    alpha = require_in_range(-0.1, "rate", minimum=0.0, maximum=1.0)
except ValueError as e:
    # Error: "rate must be in the interval [0.0, 1.0]; got -0.1"
    print(e)