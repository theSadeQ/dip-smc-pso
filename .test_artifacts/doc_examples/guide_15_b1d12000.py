# Example from: docs\optimization_simulation\guide.md
# Index: 15
# Runnable: True
# Hash: b1d12000

from src.config import load_config

# Load with unknown field rejection (strict mode)
config = load_config("config.yaml", allow_unknown=False)

# Load with unknown field warning (permissive mode)
config = load_config("config.yaml", allow_unknown=True)

# Access nested configuration
pso_cfg = config.pso
physics_cfg = config.physics
sim_cfg = config.simulation