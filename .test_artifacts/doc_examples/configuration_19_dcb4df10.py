# Example from: docs\guides\api\configuration.md
# Index: 19
# Runnable: True
# Hash: dcb4df10

try:
    config = load_config('config.yaml')
except ValueError as e:
    print(f"Validation error: {e}")
    # Check specific fields
    # Fix config.yaml
    # Reload