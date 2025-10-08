# Example from: docs\api\factory_reference.md
# Index: 3
# Runnable: True
# Hash: 8ce27d51

from src.controllers.factory import get_default_gains

gains = get_default_gains('classical_smc')
# Returns: [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]