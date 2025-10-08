# Example from: docs\factory\deprecation_management.md
# Index: 3
# Runnable: False
# Hash: 7bd05e20

# example-metadata:
# runnable: false

CLASSICAL_SMC_DEPRECATIONS = {
    'gamma': DeprecationMapping(
        old_name='gamma',
        new_name=None,
        level=DeprecationLevel.ERROR,
        message="'gamma' parameter is not valid for classical_smc. Use 'boundary_layer' instead.",
        migration_guide=(
            "Classical SMC uses 'boundary_layer' for chattering reduction, not 'gamma'. "
            "The 'gamma' parameter is specific to adaptive SMC controllers. "
            "Replace 'gamma: 0.1' with 'boundary_layer: 0.02' in your configuration."
        ),
        removed_in_version="2.0.0",
        introduced_in_version="1.8.0",
        auto_migrate=False  # Cannot auto-migrate due to semantic difference
    ),

    'adaptation_rate': DeprecationMapping(
        old_name='adaptation_rate',
        new_name=None,
        level=DeprecationLevel.ERROR,
        message="'adaptation_rate' is not valid for classical_smc. This parameter is only for adaptive_smc.",
        migration_guide=(
            "Remove 'adaptation_rate' from classical SMC configuration. "
            "If you need adaptation, use 'adaptive_smc' controller type instead."
        ),
        removed_in_version="2.0.0",
        auto_migrate=True  # Can auto-remove invalid parameter
    ),

    'switch_function': DeprecationMapping(
        old_name='switch_function',
        new_name='switch_method',
        level=DeprecationLevel.WARNING,
        message="'switch_function' parameter renamed to 'switch_method'.",
        migration_guide=(
            "Replace 'switch_function' with 'switch_method' in configuration. "
            "Valid values: 'sign', 'tanh', 'sigmoid', 'sat'. "
            "Example: switch_method: 'tanh'"
        ),
        removed_in_version="3.0.0",
        introduced_in_version="2.1.0",
        auto_migrate=True
    ),

    'K_switching': DeprecationMapping(
        old_name='K_switching',
        new_name='gains[4]',
        level=DeprecationLevel.WARNING,
        message="Separate 'K_switching' parameter deprecated. Include as 5th element in gains array.",
        migration_guide=(
            "Move K_switching value to gains array as 5th element. "
            "Example: gains: [k1, k2, λ1, λ2, K_switching, kd] "
            "Old: K_switching: 15.0, gains: [10, 5, 8, 3, 2] "
            "New: gains: [10, 5, 8, 3, 15, 2]"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True
    )
}