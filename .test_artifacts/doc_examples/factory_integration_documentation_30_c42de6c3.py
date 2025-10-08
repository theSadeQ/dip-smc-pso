# Example from: docs\factory_integration_documentation.md
# Index: 30
# Runnable: True
# Hash: c42de6c3

# Instead of many concurrent calls:
   controllers = []
   for i in range(100):
       controller = create_controller('classical_smc')  # Can cause contention
       controllers.append(controller)

   # Use batch creation:
   from src.controllers.factory import create_all_smc_controllers
   controllers = create_all_smc_controllers(gains_dict)