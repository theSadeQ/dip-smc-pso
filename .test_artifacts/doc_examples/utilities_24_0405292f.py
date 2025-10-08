# Example from: docs\guides\api\utilities.md
# Index: 24
# Runnable: True
# Hash: 0405292f

from src.utils.validation import (
    validate_physics_params,
    validate_controller_gains,
    validate_state
)

# Validate configuration
try:
    validate_physics_params(config.dip_params)
    validate_controller_gains(gains, controller_type)
    validate_state(initial_state)
    print("✅ All validation passed")
except ValueError as e:
    print(f"❌ Validation failed: {e}")
    sys.exit(1)

# Proceed with simulation
result = runner.run(controller)