# Example from: docs\controllers\factory_system_guide.md
# Index: 8
# Runnable: False
# Hash: 06b1ceff

# Priority order:
# 1. Explicitly provided gains parameter
if gains is not None:
    return gains

# 2. Config object with controller_defaults
if hasattr(config, 'controller_defaults'):
    if controller_type in config.controller_defaults:
        return config.controller_defaults[controller_type].gains

# 3. Registry default gains
return controller_info['default_gains']