# Example from: docs\factory\factory_integration_user_guide.md
# Index: 11
# Runnable: True
# Hash: 3ac77e99

from src.controllers.factory.deprecation import check_deprecated_config

# Automatic migration of deprecated parameters
old_config = {
    'gamma': 0.1,  # Invalid for classical SMC
    'switch_function': 'sign',  # Old parameter name
    'K_switching': 2.0  # Separate switching gain
}

# Migrate deprecated parameters
migrated_config = check_deprecated_config('classical_smc', old_config)
print("Migrated config:", migrated_config)
# Output: Migrated config: {'switch_method': 'sign'}
# Warning: Removed invalid 'gamma' parameter for classical_smc