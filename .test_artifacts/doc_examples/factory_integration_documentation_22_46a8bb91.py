# Example from: docs\factory_integration_documentation.md
# Index: 22
# Runnable: True
# Hash: 46a8bb91

from src.controllers.factory import CONTROLLER_REGISTRY
   controller_info = CONTROLLER_REGISTRY['mpc_controller']
   if controller_info['class'] is None:
       print("Controller not available - check dependencies")