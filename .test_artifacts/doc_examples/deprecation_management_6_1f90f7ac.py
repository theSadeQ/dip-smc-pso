# Example from: docs\factory\deprecation_management.md
# Index: 6
# Runnable: False
# Hash: 1f90f7ac

# example-metadata:
# runnable: false

HYBRID_SMC_DEPRECATIONS = {
    'mode': DeprecationMapping(
        old_name='mode',
        new_name='hybrid_mode',
        level=DeprecationLevel.WARNING,
        message="'mode' parameter renamed to 'hybrid_mode'.",
        migration_guide=(
            "Replace 'mode' with 'hybrid_mode' and use HybridMode enum values. "
            "Available modes: 'CLASSICAL_ADAPTIVE', 'ADAPTIVE_STA', 'CLASSICAL_STA'. "
            "Example: hybrid_mode: 'CLASSICAL_ADAPTIVE'"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True
    ),

    'switch_threshold': DeprecationMapping(
        old_name='switch_threshold',
        new_name='switching_criteria',
        level=DeprecationLevel.WARNING,
        message="'switch_threshold' renamed to 'switching_criteria' with enhanced functionality.",
        migration_guide=(
            "Replace 'switch_threshold' with 'switching_criteria' configuration. "
            "New format supports multiple criteria: error_threshold, time_threshold, performance_threshold. "
            "Example: switching_criteria: {error_threshold: 0.1, time_threshold: 2.0}"
        ),
        removed_in_version="3.0.0",
        auto_migrate=False  # Requires manual migration due to format change
    ),

    'sub_controller_gains': DeprecationMapping(
        old_name='sub_controller_gains',
        new_name=['classical_config', 'adaptive_config'],
        level=DeprecationLevel.ERROR,
        message="'sub_controller_gains' replaced with full sub-controller configurations.",
        migration_guide=(
            "Replace 'sub_controller_gains' with complete 'classical_config' and 'adaptive_config' objects. "
            "This provides full parameter control for each sub-controller. "
            "See hybrid SMC configuration examples in documentation."
        ),
        removed_in_version="2.0.0",
        auto_migrate=False
    )
}