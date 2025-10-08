# Example from: docs\guides\tutorials\tutorial-04-custom-controller.md
# Index: 8
# Runnable: False
# Hash: 6bced852

# example-metadata:
# runnable: false

def __init__(self, gains, ...):
    # Check count
    if len(gains) != expected_count:
        raise ValueError(f"Expected {expected_count} gains, got {len(gains)}")

    # Check bounds
    if any(g < 0 for g in gains[:4]):  # Surface gains must be positive
        raise ValueError("Surface gains must be non-negative")

    # Check constraints (e.g., exponents in (0,1))
    if not (0 < alpha < 1):
        raise ValueError(f"Exponent α must be in (0,1), got {alpha}")