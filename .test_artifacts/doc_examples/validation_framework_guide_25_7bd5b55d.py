# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 25
# Runnable: True
# Hash: 7bd5b55d

# Enable validation warnings during development
import logging
logging.basicConfig(level=logging.DEBUG)

try:
    gains = [10.0, -5.0, 8.0, 3.0, 15.0, 2.0]
    result = validator.validate_gains(gains, "classical")
except ValueError as e:
    # Print detailed context
    print(f"Validation failed: {e}")
    print(f"Provided gains: {gains}")
    print(f"Expected bounds: {validator.get_recommended_ranges('classical')}")