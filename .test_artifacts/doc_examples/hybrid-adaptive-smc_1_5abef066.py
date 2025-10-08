# Example from: docs\reference\controllers\hybrid-adaptive-smc.md
# Index: 1
# Runnable: True
# Hash: 5abef066

from src.controllers.factory import create_controller
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller
controller = create_controller('hybrid_adaptive_sta_smc', config)

# Simulation loop
for t, state in simulation:
    u = controller.compute_control(state, reference, t)

    # Monitor adaptive gains
    k1, k2 = controller.get_adaptive_gains()
    print(f"Adaptive gains: k1={k1:.3f}, k2={k2:.3f}")