# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 3
# Runnable: True
# Hash: 54c251d5

_controller_registry: Dict[SMCType, Callable] = {}

def register_controller(ctrl_type: SMCType, factory_fn: Callable):
    _controller_registry[ctrl_type] = factory_fn