# Example from: docs\factory\factory_api_reference.md
# Index: 24
# Runnable: True
# Hash: 87347bbb

from src.controllers.factory import SMCType

# Type-safe controller specification
controller_type = SMCType.CLASSICAL
factory_func = create_pso_controller_factory(controller_type)