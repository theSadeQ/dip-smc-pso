# Example from: docs\api\phase_4_2_completion_report.md
# Index: 4
# Runnable: True
# Hash: effff73b

try:
    _validate_controller_gains(controller_gains, controller_info, controller_type)
except ValueError as e:
    if gains is None:  # Only auto-fix defaults
        if controller_type == 'sta_smc':
            controller_gains = [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]  # K1=25 > K2=15
        _validate_controller_gains(controller_gains, controller_info, controller_type)
    else:
        raise e  # User-provided gains, do not auto-correct