# Example from: docs\PATTERNS.md
# Index: 16
# Runnable: False
# Hash: f2317dfc

# example-metadata:
# runnable: false

# src/utils/validation/parameter_validators.py

def validate_gains(n_expected: int):
    """Decorator to validate gain array length."""
    def decorator(func):
        def wrapper(self, gains, *args, **kwargs):
            if len(gains) != n_expected:
                raise ValueError(f"Expected {n_expected} gains, got {len(gains)}")
            return func(self, gains, *args, **kwargs)
        return wrapper
    return decorator

# Usage
class ClassicalSMC:
    @validate_gains(n_expected=6)
    def __init__(self, gains):
        self.gains = gains  # Guaranteed to have 6 elements