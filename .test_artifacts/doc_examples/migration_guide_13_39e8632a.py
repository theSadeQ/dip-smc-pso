# Example from: docs\factory\migration_guide.md
# Index: 13
# Runnable: False
# Hash: 39e8632a

def convert_legacy_format(old_config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert legacy configuration format to new structure."""

    new_config = {}

    # Handle legacy controller_defaults structure
    if 'controller_defaults' in old_config:
        new_config['controllers'] = old_config['controller_defaults']

    # Handle direct controller configuration
    elif 'controllers' not in old_config:
        # Assume root-level controller configuration
        controllers = {}
        for key, value in old_config.items():
            if key in ['classical_smc', 'adaptive_smc', 'sta_smc', 'hybrid_adaptive_sta_smc']:
                controllers[key] = value

        if controllers:
            new_config['controllers'] = controllers
        else:
            new_config = old_config
    else:
        new_config = old_config

    return new_config