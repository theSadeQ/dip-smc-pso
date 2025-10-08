# Example from: docs\guides\api\configuration.md
# Index: 12
# Runnable: True
# Hash: 6351071d

import os
from src.config import load_config

# Use environment variable for config selection
config_file = os.getenv('DIP_CONFIG', 'config.yaml')
config = load_config(config_file)

# Override parameters from environment
if os.getenv('DIP_FULL_DYNAMICS'):
    config.simulation.use_full_dynamics = True

if os.getenv('DIP_DURATION'):
    config.simulation.duration = float(os.getenv('DIP_DURATION'))