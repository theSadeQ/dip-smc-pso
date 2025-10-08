# Example from: docs\controllers\factory_system_guide.md
# Index: 26
# Runnable: False
# Hash: 3ee59110

# example-metadata:
# runnable: false

# Invalid default gains are automatically corrected
controller_gains = [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]

try:
    _validate_controller_gains(controller_gains, controller_info, 'sta_smc')
except ValueError as e:
    if gains is None:  # Only auto-fix if using default gains
        if controller_type == 'sta_smc':
            # Fix K1 > K2 requirement
            controller_gains = [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]  # K1=25 > K2=15

        # Re-validate after fix
        _validate_controller_gains(controller_gains, controller_info, controller_type)