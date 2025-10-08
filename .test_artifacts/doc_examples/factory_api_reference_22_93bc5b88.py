# Example from: docs\factory\factory_api_reference.md
# Index: 22
# Runnable: True
# Hash: 93bc5b88

from src.controllers.factory import SMCType, validate_smc_gains

gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
is_valid = validate_smc_gains(SMCType.CLASSICAL, gains)
print(f"Gains valid: {is_valid}")