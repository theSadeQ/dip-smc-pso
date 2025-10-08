# Example from: docs\factory\factory_api_reference.md
# Index: 28
# Runnable: True
# Hash: 86aa4d6c

from src.controllers.factory.deprecation import check_deprecated_config

old_config = {
    'switch_function': 'sign',  # Old parameter name
    'gamma': 0.1  # Invalid for classical SMC
}

migrated_config = check_deprecated_config('classical_smc', old_config)
# Result: {'switch_method': 'sign'}
# Warning: Removed invalid 'gamma' parameter