# Example from: docs\guides\api\configuration.md
# Index: 3
# Runnable: True
# Hash: 44a4c728

# Reject any extra fields not in schema
config = load_config('config.yaml', allow_unknown=False)