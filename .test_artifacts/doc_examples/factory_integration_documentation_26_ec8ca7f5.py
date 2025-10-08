# Example from: docs\factory_integration_documentation.md
# Index: 26
# Runnable: True
# Hash: ec8ca7f5

from src.controllers.factory import validate_smc_gains, SMCType

   is_valid = validate_smc_gains(SMCType.CLASSICAL, gains)
   if not is_valid:
       print("Gains failed validation")