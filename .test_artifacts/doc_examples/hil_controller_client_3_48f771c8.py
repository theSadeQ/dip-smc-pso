# Example from: docs\reference\interfaces\hil_controller_client.md
# Index: 3
# Runnable: True
# Hash: 48f771c8

from src.interfaces.hil import HILControllerClient
import time

# Client with aggressive timeout
client = HILControllerClient(
    cfg=config,
    plant_addr=("127.0.0.1", 5555),
    bind_addr=("127.0.0.1", 0),
    dt=0.01,
    steps=5000,
    recv_timeout_s=0.5  # 500 ms timeout
)

# Monitor fallback activations
fallback_count = 0
original_run = client.run

def monitored_run():
    global fallback_count
    # Count timeout events
    try:
        original_run()
    except TimeoutError:
        fallback_count += 1
        print(f"Fallback controller activated: {fallback_count} times")

client.run = monitored_run
client.run()

print(f"Total fallback activations: {fallback_count}")