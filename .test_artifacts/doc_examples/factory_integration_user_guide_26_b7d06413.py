# Example from: docs\factory\factory_integration_user_guide.md
# Index: 26
# Runnable: True
# Hash: b7d06413

from src.controllers.factory.deprecation import check_deprecated_config

# Migrate old configuration format
old_config = {
    'K_switching': 2.0,
    'gamma': 0.1,  # Invalid for classical SMC
    'switch_function': 'sign'
}

# Automatic migration with warnings
migrated_config = check_deprecated_config('classical_smc', old_config)