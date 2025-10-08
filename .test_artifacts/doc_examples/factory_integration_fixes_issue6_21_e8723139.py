# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 21
# Runnable: True
# Hash: e8723139

from src.controllers.factory import validate_smc_gains

# Validate gains before creating controller
gains = [15.0, 12.0, 8.0, 6.0, 25.0, 4.0]
is_valid = validate_smc_gains(SMCType.CLASSICAL, gains)

if is_valid:
    controller = create_controller('classical_smc', gains=gains)
else:
    print("Invalid gains provided")