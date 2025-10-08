# Example from: docs\reference\utils\validation___init__.md
# Index: 4
# Runnable: True
# Hash: 109d1390

from src.utils.validation import require_in_range, require_positive
import numpy as np

def validate_controller_parameters(params: dict):
    # Multiple constraint validation
    validated = {}

    # Gains must be positive
    for gain_name in ['k1', 'k2', 'k3']:
        validated[gain_name] = require_positive(
            params[gain_name], name=gain_name
        )

    # Max force in specific range
    validated['max_force'] = require_in_range(
        params['max_force'], min_val=10.0, max_val=200.0,
        name="max_force"
    )

    # Boundary layer must be small positive
    validated['boundary_layer'] = require_in_range(
        params['boundary_layer'], min_val=0.0, max_val=1.0,
        name="boundary_layer"
    )

    return validated

# Validate complete parameter set
params = {
    'k1': 10.0, 'k2': 8.0, 'k3': 15.0,
    'max_force': 100.0,
    'boundary_layer': 0.01
}
valid_params = validate_controller_parameters(params)  # ✓ All pass