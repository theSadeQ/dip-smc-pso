# Example from: docs\factory_integration_documentation.md
# Index: 23
# Runnable: True
# Hash: 7bd3d7bc

try:
       from src.controllers.mpc.controller import MPCController
       print("MPC controller available")
   except ImportError as e:
       print(f"MPC controller not available: {e}")