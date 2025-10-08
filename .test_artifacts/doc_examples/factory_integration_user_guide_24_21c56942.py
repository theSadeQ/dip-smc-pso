# Example from: docs\factory\factory_integration_user_guide.md
# Index: 24
# Runnable: True
# Hash: 21c56942

# Validate gains before use
def validate_gains(gains):
    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive")
    return gains

validated_gains = validate_gains([20.0, 15.0, 12.0, 8.0, 35.0, 5.0])