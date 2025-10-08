# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 4
# Runnable: True
# Hash: 26cdcab7

_registry_lock = threading.Lock()

with _registry_lock:
    _controller_registry[ctrl_type] = factory_fn