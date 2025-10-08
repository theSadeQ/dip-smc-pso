# Example from: docs\reference\utils\validation___init__.md
# Index: 2
# Runnable: True
# Hash: fe3a99b9

from src.utils.validation import require_positive

def configure_pendulum(mass: float, length: float):
    # Physical parameters must be positive
    m = require_positive(mass, name="mass")
    L = require_positive(length, name="length")

    # Compute inertia
    I = m * L**2
    return I

# Valid parameters
I = configure_pendulum(1.0, 0.5)  # ✓ Returns 0.25

# Invalid parameters
try:
    I = configure_pendulum(-1.0, 0.5)  # ValueError: must be positive
except ValueError as e:
    print(f"Invalid mass: {e}")