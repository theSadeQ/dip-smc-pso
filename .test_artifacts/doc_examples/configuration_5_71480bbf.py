# Example from: docs\guides\api\configuration.md
# Index: 5
# Runnable: True
# Hash: 71480bbf

import yaml
from src.config.schemas import DIPParams, SimulationConfig

# Load only specific sections
with open('config.yaml', 'r') as f:
    config_dict = yaml.safe_load(f)

# Create partial config objects
physics = DIPParams(**config_dict['dip_params'])
sim_settings = SimulationConfig(**config_dict['simulation'])