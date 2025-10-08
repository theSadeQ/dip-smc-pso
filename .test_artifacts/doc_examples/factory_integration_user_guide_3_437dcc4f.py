# Example from: docs\factory\factory_integration_user_guide.md
# Index: 3
# Runnable: True
# Hash: 437dcc4f

import threading
from src.controllers.factory import create_controller

def create_controllers_concurrently():
    """Safe concurrent controller creation."""
    controllers = []

    def worker(controller_type, gains):
        # Thread-safe factory operations
        controller = create_controller(controller_type, gains=gains)
        controllers.append(controller)

    # Multiple threads can safely use the factory
    threads = []
    for i in range(10):
        thread = threading.Thread(
            target=worker,
            args=('classical_smc', [20.0, 15.0, 12.0, 8.0, 35.0, 5.0])
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return controllers