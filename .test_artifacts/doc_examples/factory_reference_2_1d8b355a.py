# Example from: docs\api\factory_reference.md
# Index: 2
# Runnable: True
# Hash: 1d8b355a

from src.controllers.factory import list_available_controllers

available = list_available_controllers()
# Returns: ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']