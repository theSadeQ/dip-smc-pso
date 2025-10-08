# Example from: docs\guides\api\utilities.md
# Index: 4
# Runnable: True
# Hash: c1704d31

from src.utils.validation import validate_controller_gains

gains = [10, 8, 15, 12, 50, 5]
controller_type = 'classical_smc'

is_valid = validate_controller_gains(gains, controller_type)

# Checks:
# - Correct number of gains
# - All gains positive (where required)
# - Gains within reasonable bounds