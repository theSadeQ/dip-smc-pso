# Example from: docs\reference\interfaces\hil_controller_client.md
# Index: 5
# Runnable: False
# Hash: 1293d668

from src.interfaces.hil import HILControllerClient
import time

def run_client_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            client = HILControllerClient(
                cfg=config,
                plant_addr=("127.0.0.1", 5555),
                bind_addr=("127.0.0.1", 0),
                dt=0.01,
                steps=5000
            )
            client.run()
            print(f"Success on attempt {attempt + 1}")
            return
        except ConnectionError as e:
            print(f"Connection failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print("All retry attempts failed")

run_client_with_retry()