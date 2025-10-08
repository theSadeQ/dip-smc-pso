# Example from: docs\controllers\factory_system_guide.md
# Index: 31
# Runnable: False
# Hash: e930ca49

# example-metadata:
# runnable: false

# 1. Specific exception types
class FactoryConfigurationError(ValueError):
    pass

# 2. Informative error messages
raise ValueError(
    f"Controller '{controller_info.get('description', 'unknown')}' "
    f"requires {expected_count} gains, got {len(gains)}"
)

# 3. Graceful fallback
try:
    controller_config = config_class(**config_params)
except Exception as e:
    logger.debug(f"Could not create full config, using minimal config: {e}")
    controller_config = config_class(**fallback_params)