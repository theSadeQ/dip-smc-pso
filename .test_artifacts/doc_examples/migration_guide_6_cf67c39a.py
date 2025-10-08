# Example from: docs\factory\migration_guide.md
# Index: 6
# Runnable: False
# Hash: cf67c39a

# example-metadata:
# runnable: false

def migrate_adaptive_smc_manually(old_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Manual migration procedure for Adaptive SMC configurations.

    Changes:
    1. Combine gains and adaptation_gain into 5-element gains array
    2. Rename 'boundary_layer_thickness' to 'boundary_layer'
    3. Split 'estimate_bounds' into 'K_min' and 'K_max'
    4. Rename 'adaptation_law' to 'alpha'
    """

    new_config = {}

    # Step 1: Handle gains array with gamma (adaptation rate)
    gains = old_config.get('gains', [12.0, 10.0, 6.0, 5.0])

    # If gains has only 4 elements, add adaptation_gain as 5th element
    if len(gains) == 4:
        adaptation_gain = old_config.get('adaptation_gain', 2.5)
        gains = gains + [adaptation_gain]
    elif len(gains) < 4:
        # Fill missing gains with defaults
        default_gains = [12.0, 10.0, 6.0, 5.0, 2.5]
        gains = gains + default_gains[len(gains):]

    new_config['gains'] = gains[:5]  # Ensure exactly 5 gains

    # Step 2: Handle renamed parameters
    renames = {
        'boundary_layer_thickness': 'boundary_layer',
        'adaptation_law': 'alpha'
    }

    for old_name, new_name in renames.items():
        if old_name in old_config:
            new_config[new_name] = old_config[old_name]
            print(f"Migrated: {old_name} -> {new_name}")

    # Step 3: Handle split parameters
    if 'estimate_bounds' in old_config:
        bounds = old_config['estimate_bounds']
        if isinstance(bounds, (list, tuple)) and len(bounds) == 2:
            new_config['K_min'] = bounds[0]
            new_config['K_max'] = bounds[1]
            print(f"Split: estimate_bounds -> K_min, K_max")
        else:
            print(f"Warning: Invalid estimate_bounds format, using defaults")
            new_config['K_min'] = 0.1
            new_config['K_max'] = 100.0

    # Step 4: Copy valid parameters
    valid_params = [
        'max_force', 'dt', 'boundary_layer', 'leak_rate', 'adapt_rate_limit',
        'K_min', 'K_max', 'K_init', 'alpha', 'dead_zone', 'smooth_switch',
        'dynamics_model'
    ]

    for param in valid_params:
        if param in old_config:
            new_config[param] = old_config[param]

    # Step 5: Ensure required parameters have defaults
    new_config.setdefault('max_force', 150.0)
    new_config.setdefault('dt', 0.001)
    new_config.setdefault('boundary_layer', 0.01)
    new_config.setdefault('leak_rate', 0.01)
    new_config.setdefault('adapt_rate_limit', 10.0)
    new_config.setdefault('K_min', 0.1)
    new_config.setdefault('K_max', 100.0)
    new_config.setdefault('K_init', 10.0)
    new_config.setdefault('alpha', 0.5)

    return new_config

# Example usage
old_adaptive_config = {
    'gains': [12, 10, 6, 5],
    'adaptation_gain': 2.5,
    'boundary_layer_thickness': 0.02,
    'estimate_bounds': [0.1, 100.0],
    'adaptation_law': 0.5,
    'max_force': 150.0
}

new_adaptive_config = migrate_adaptive_smc_manually(old_adaptive_config)
print("Migrated Adaptive SMC config:", new_adaptive_config)