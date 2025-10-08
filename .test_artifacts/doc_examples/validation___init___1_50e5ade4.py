# Example from: docs\reference\utils\validation___init__.md
# Index: 1
# Runnable: True
# Hash: 50e5ade4

from src.utils.validation import require_in_range

def set_control_gain(gain: float):
    # Validate gain is in acceptable range
    validated_gain = require_in_range(
        gain, min_val=0.1, max_val=100.0,
        name="control_gain"
    )
    return validated_gain

# Valid gain
k = set_control_gain(10.0)  # ✓ Returns 10.0

# Invalid gain
try:
    k = set_control_gain(150.0)  # ValueError: out of range
except ValueError as e:
    print(f"Validation failed: {e}")