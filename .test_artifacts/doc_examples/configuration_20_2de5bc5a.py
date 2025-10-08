# Example from: docs\guides\api\configuration.md
# Index: 20
# Runnable: True
# Hash: 2de5bc5a

# Use strict validation to catch typos
config = load_config('config.yaml', allow_unknown=False)
# Will raise error if unknown fields present