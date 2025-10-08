# Example from: docs\factory\factory_api_reference.md
# Index: 34
# Runnable: True
# Hash: c99d0486

# Optimized batch controller creation
import concurrent.futures
from src.controllers.factory import create_controller

def create_controllers_optimized(controller_specs):
    """Optimized parallel controller creation."""

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(create_controller, **spec): name
            for name, spec in controller_specs.items()
        }

        controllers = {}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                controllers[name] = future.result(timeout=30)
            except Exception as e:
                print(f"Failed to create {name}: {e}")

        return controllers