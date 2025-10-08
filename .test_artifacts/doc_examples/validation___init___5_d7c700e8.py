# Example from: docs\reference\utils\validation___init__.md
# Index: 5
# Runnable: True
# Hash: d7c700e8

from src.utils.validation import require_positive, require_in_range
import numpy as np

def validate_gains_array(gains: np.ndarray):
    \"\"\"Validate array of controller gains.\"\"\"
    # Check array dimensions
    if gains.shape[0] != 6:
        raise ValueError(f"Expected 6 gains, got {gains.shape[0]}")

    # Validate each gain individually
    for i, gain in enumerate(gains):
        if i < 5:  # First 5 gains must be positive
            require_positive(gain, name=f"gain[{i}]")
        else:  # Last gain can be zero or positive
            require_in_range(gain, min_val=0.0, max_val=100.0,
                           name=f"gain[{i}]")

    return gains

# Valid gains
gains = np.array([10.0, 8.0, 15.0, 12.0, 50.0, 5.0])
validated_gains = validate_gains_array(gains)  # ✓ Pass

# Invalid gains
try:
    bad_gains = np.array([10.0, -8.0, 15.0, 12.0, 50.0, 5.0])
    validate_gains_array(bad_gains)  # ValueError: negative gain
except ValueError as e:
    print(f"Validation error: {e}")