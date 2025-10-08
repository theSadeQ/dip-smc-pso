# Example from: docs\controllers\factory_system_guide.md
# Index: 20
# Runnable: True
# Hash: 8db209b0

from src.controllers.factory.deprecation import check_deprecated_config

# Automatic migration of deprecated parameters
controller_params = check_deprecated_config(controller_type, controller_params)

# Example migration:
# Old: {'switching_gain': 50.0}
# New: {'K': 50.0}