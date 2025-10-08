# Example from: docs\guides\api\configuration.md
# Index: 2
# Runnable: True
# Hash: e8e418b4

try:
    config = load_config('config.yaml')
    print("Configuration valid!")
except ValueError as e:
    print(f"Configuration error: {e}")