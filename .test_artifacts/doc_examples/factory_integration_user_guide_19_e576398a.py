# Example from: docs\factory\factory_integration_user_guide.md
# Index: 19
# Runnable: True
# Hash: e576398a

import concurrent.futures
from src.controllers.factory import create_controller

def create_controllers_parallel(controller_specs, config, max_workers=4):
    """Create multiple controllers in parallel."""

    def create_single(spec):
        controller_type, params = spec
        return create_controller(controller_type, config=config, **params)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(create_single, spec)
            for spec in controller_specs.items()
        ]

        controllers = {}
        for future, (controller_type, _) in zip(futures, controller_specs.items()):
            try:
                controllers[controller_type] = future.result(timeout=30)
            except Exception as e:
                print(f"Failed to create {controller_type}: {e}")

    return controllers