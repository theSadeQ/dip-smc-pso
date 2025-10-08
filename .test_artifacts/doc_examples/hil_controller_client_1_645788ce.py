# Example from: docs\reference\interfaces\hil_controller_client.md
# Index: 1
# Runnable: True
# Hash: 645788ce

from src.interfaces.hil import HILControllerClient
from src.config import load_config

# Load configuration
config = load_config("config.yaml")

# Connect to HIL server
client = HILControllerClient(
    cfg=config,
    plant_addr=("127.0.0.1", 5555),
    bind_addr=("127.0.0.1", 0),  # Auto-assign port
    dt=0.01,
    steps=5000,
    results_path="hil_results.json"
)

# Run HIL simulation
client.run()

print("HIL simulation complete, results saved to hil_results.json")