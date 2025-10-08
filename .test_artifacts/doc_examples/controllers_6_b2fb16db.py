# Example from: docs\guides\api\controllers.md
# Index: 6
# Runnable: True
# Hash: b2fb16db

from src.controllers import validate_smc_gains

# Validate gains before simulation
gains = [10, 8, 15, 12, 50, 5]
is_valid = validate_smc_gains(SMCType.CLASSICAL, gains)

if not is_valid:
    raise ValueError("Invalid gains for Classical SMC")

# Validation checks:
# - Correct number of gains for controller type
# - All gains positive (except epsilon can be 0)
# - Gains within physical bounds