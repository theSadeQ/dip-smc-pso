# Example from: docs\guides\api\configuration.md
# Index: 11
# Runnable: True
# Hash: 2d4f62e1

def merge_configs(base_config, override_config):
    """Merge two configurations, with override taking precedence."""
    import copy
    merged = copy.deepcopy(base_config)

    # Override physics params if specified
    if override_config.dip_params is not None:
        merged.dip_params = override_config.dip_params

    # Override simulation settings
    if override_config.simulation is not None:
        merged.simulation = override_config.simulation

    # Merge controller configs
    for ctrl_name, ctrl_config in override_config.controllers.items():
        merged.controllers[ctrl_name] = ctrl_config

    return merged

# Usage
base = load_config('config.yaml')
override = load_config('config_override.yaml')
final_config = merge_configs(base, override)