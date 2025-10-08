# Example from: docs\factory\factory_api_reference.md
# Index: 31
# Runnable: True
# Hash: 5f3c1a5c

import threading
from src.controllers.factory import create_controller

def worker_thread(thread_id):
    """Thread-safe controller creation."""
    controller = create_controller(
        'classical_smc',
        gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
    )
    # Each thread gets independent controller instance
    return controller

# Safe concurrent execution
threads = []
for i in range(10):
    thread = threading.Thread(target=worker_thread, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()