# Example from: docs\guides\api\configuration.md
# Index: 1
# Runnable: True
# Hash: 2fa7a6af

from src.config import load_config

# Load from default config.yaml
config = load_config('config.yaml')

# Access configuration sections
physics = config.dip_params
controllers = config.controllers
simulation = config.simulation
pso = config.pso