# Example from: docs\guides\api\configuration.md
# Index: 16
# Runnable: True
# Hash: 39bac9f9

import os

env = os.getenv('ENVIRONMENT', 'development')
config_file = f'config_{env}.yaml'
config = load_config(config_file)