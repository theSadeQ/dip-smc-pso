# Example from: docs\api\factory_system_api_reference.md
# Index: 55
# Runnable: False
# Hash: ee5825bd

# example-metadata:
# runnable: false

try:
    _validate_controller_gains(controller_gains, controller_info, controller_type)
except ValueError as e:
    # For invalid default gains, try to fix them automatically
    if gains is None:  # Only auto-fix if using default gains
        if controller_type == 'sta_smc':
            # Fix K1 > K2 requirement
            controller_gains = [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]
        elif controller_type == 'adaptive_smc':
            # Fix 5-gain requirement
            controller_gains = [25.0, 18.0, 15.0, 10.0, 4.0]
        else:
            raise e  # Cannot auto-fix, re-raise exception

        # Re-validate after fix
        _validate_controller_gains(controller_gains, controller_info, controller_type)
    else:
        raise e  # User-provided gains, do not auto-correct