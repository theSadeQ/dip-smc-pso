# Example from: docs\api\factory_reference.md
# Index: 11
# Runnable: True
# Hash: 13a5e0e9

import threading
from src.controllers.factory import create_controller

def create_controllers_concurrently():
    controller = create_controller('classical_smc')
    # Safe for concurrent execution

threads = [threading.Thread(target=create_controllers_concurrently) for _ in range(10)]
for t in threads:
    t.start()