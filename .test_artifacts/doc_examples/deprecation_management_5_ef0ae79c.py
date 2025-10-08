# Example from: docs\factory\deprecation_management.md
# Index: 5
# Runnable: False
# Hash: ef0ae79c

STA_SMC_DEPRECATIONS = {
    'K1': DeprecationMapping(
        old_name='K1',
        new_name='gains[0]',
        level=DeprecationLevel.WARNING,
        message="Separate K1/K2 parameters deprecated. Use gains array instead.",
        migration_guide=(
            "Include K1, K2 as first two elements in gains array: [K1, K2, k1, k2, lam1, lam2]. "
            "This provides consistent parameter interface across all SMC controllers. "
            "Example: gains: [35.0, 20.0, 25.0, 18.0, 12.0, 8.0]"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True
    ),

    'K2': DeprecationMapping(
        old_name='K2',
        new_name='gains[1]',
        level=DeprecationLevel.WARNING,
        message="Separate K1/K2 parameters deprecated. Use gains array instead.",
        migration_guide=(
            "Include K1, K2 as first two elements in gains array: [K1, K2, k1, k2, lam1, lam2]. "
            "Ensure K1 > K2 for optimal STA performance. "
            "Example: gains: [35.0, 20.0, 25.0, 18.0, 12.0, 8.0]"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True
    ),

    'alpha_power': DeprecationMapping(
        old_name='alpha_power',
        new_name='power_exponent',
        level=DeprecationLevel.WARNING,
        message="'alpha_power' parameter renamed to 'power_exponent' for clarity.",
        migration_guide=(
            "Replace 'alpha_power' with 'power_exponent'. "
            "Standard STA uses power_exponent: 0.5 for finite-time convergence. "
            "Valid range: (0, 1). Example: power_exponent: 0.5"
        ),
        removed_in_version="3.0.0",
        auto_migrate=True,
        validation_function=lambda x: 0.0 < x < 1.0
    ),

    'switching_function_type': DeprecationMapping(
        old_name='switching_function_type',
        new_name='switch_method',
        level=DeprecationLevel.INFO,
        message="'switching_function_type' renamed to 'switch_method' for consistency.",
        migration_guide=(
            "Replace 'switching_function_type' with 'switch_method'. "
            "Valid options: 'tanh', 'sigmoid', 'sat'. "
            "STA-SMC typically uses 'tanh' for smooth switching."
        ),
        removed_in_version="4.0.0",
        auto_migrate=True
    )
}