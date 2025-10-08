# Example from: docs\controllers\mpc_technical_guide.md
# Index: 25
# Runnable: True
# Hash: 77c7d191

from src.controllers.factory import create_controller

# Create MPC via factory (if supported)
config = load_config("config.yaml")

controller = create_controller(
    'mpc_controller',
    config=config,
    # MPC-specific parameters
    horizon=20,
    dt=0.02,
    max_force=20.0
)