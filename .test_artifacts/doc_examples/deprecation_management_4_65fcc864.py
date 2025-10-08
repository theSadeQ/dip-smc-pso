# Example from: docs\factory\deprecation_management.md
# Index: 4
# Runnable: False
# Hash: 65fcc864

ADAPTIVE_SMC_DEPRECATIONS = {
    'boundary_layer_thickness': DeprecationMapping(
        old_name='boundary_layer_thickness',
        new_name='boundary_layer',
        level=DeprecationLevel.WARNING,
        message="'boundary_layer_thickness' parameter renamed to 'boundary_layer'.",
        migration_guide=(
            "Replace 'boundary_layer_thickness' with 'boundary_layer' in configuration. "
            "The parameter has the same meaning and value range (0.001 to 0.1). "
            "Example: boundary_layer: 0.01"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True
    ),

    'adaptation_gain': DeprecationMapping(
        old_name='adaptation_gain',
        new_name='gains[4]',
        level=DeprecationLevel.WARNING,
        message="'adaptation_gain' parameter renamed to 'gamma' (included in gains array).",
        migration_guide=(
            "Remove separate 'adaptation_gain' and include gamma as 5th element in gains array. "
            "The adaptation gain (gamma) controls parameter estimation rate. "
            "Example: gains: [k1, k2, λ1, λ2, gamma] where gamma = old adaptation_gain"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True,
        validation_function=lambda x: 0.01 <= x <= 10.0
    ),

    'estimate_bounds': DeprecationMapping(
        old_name='estimate_bounds',
        new_name=['K_min', 'K_max'],
        level=DeprecationLevel.WARNING,
        message="'estimate_bounds' parameter split into 'K_min' and 'K_max'.",
        migration_guide=(
            "Replace 'estimate_bounds: [min, max]' with separate 'K_min' and 'K_max' parameters. "
            "Example: K_min: 0.1, K_max: 100.0"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True
    ),

    'adaptation_law': DeprecationMapping(
        old_name='adaptation_law',
        new_name='alpha',
        level=DeprecationLevel.INFO,
        message="'adaptation_law' parameter renamed to 'alpha' for clarity.",
        migration_guide=(
            "Replace 'adaptation_law' with 'alpha'. "
            "The parameter controls adaptation law exponent (typically 0.5 for standard adaptation). "
            "Example: alpha: 0.5"
        ),
        removed_in_version="4.0.0",
        auto_migrate=True
    )
}