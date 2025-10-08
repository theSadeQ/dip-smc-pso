# Example from: docs\factory_integration_documentation.md
# Index: 24
# Runnable: True
# Hash: 1dfebc51

from src.controllers.factory import get_default_gains
   default_gains = get_default_gains('classical_smc')
   print(f"Required gains: {len(default_gains)}")
   print(f"Default values: {default_gains}")