# Example from: docs\factory\README.md
# Index: 3
# Runnable: True
# Hash: 4a22ad40

from src.controllers.factory.deprecation import check_deprecated_config

# Automatic parameter migration
old_config = {'switch_function': 'sign', 'gamma': 0.1}
new_config = check_deprecated_config('classical_smc', old_config)