# Example from: docs\factory\migration_guide.md
# Index: 7
# Runnable: False
# Hash: b145a062

def migrate_sta_smc_manually(old_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Manual migration procedure for Super-Twisting SMC configurations.

    Changes:
    1. Combine K1, K2, and other gains into 6-element gains array
    2. Rename 'alpha_power' to 'power_exponent'
    3. Rename 'switching_function_type' to 'switch_method'
    """

    new_config = {}

    # Step 1: Handle gains array with K1, K2 integration
    gains = old_config.get('gains', [])

    # If K1 and K2 are separate parameters, integrate them
    if 'K1' in old_config and 'K2' in old_config:
        K1 = old_config['K1']
        K2 = old_config['K2']

        # If gains array exists, assume it contains [k1, k2, lam1, lam2]
        if len(gains) >= 4:
            gains = [K1, K2] + gains[:4]
        else:
            # Create full gains array
            default_surface_gains = [25.0, 18.0, 12.0, 8.0]
            surface_gains = gains + default_surface_gains[len(gains):]
            gains = [K1, K2] + surface_gains[:4]

        print(f"Integrated: K1={K1}, K2={K2} into gains array")

    elif len(gains) < 6:
        # Fill missing gains with defaults
        default_gains = [35.0, 20.0, 25.0, 18.0, 12.0, 8.0]
        gains = gains + default_gains[len(gains):]

    new_config['gains'] = gains[:6]  # Ensure exactly 6 gains

    # Step 2: Handle renamed parameters
    renames = {
        'alpha_power': 'power_exponent',
        'switching_function_type': 'switch_method'
    }

    for old_name, new_name in renames.items():
        if old_name in old_config:
            new_config[new_name] = old_config[old_name]
            print(f"Migrated: {old_name} -> {new_name}")

    # Step 3: Copy valid parameters
    valid_params = [
        'max_force', 'dt', 'power_exponent', 'regularization',
        'boundary_layer', 'switch_method', 'damping_gain', 'dynamics_model'
    ]

    for param in valid_params:
        if param in old_config:
            new_config[param] = old_config[param]

    # Step 4: Ensure required parameters have defaults
    new_config.setdefault('max_force', 150.0)
    new_config.setdefault('dt', 0.001)
    new_config.setdefault('power_exponent', 0.5)
    new_config.setdefault('regularization', 1e-6)
    new_config.setdefault('boundary_layer', 0.01)
    new_config.setdefault('switch_method', 'tanh')

    return new_config

# Example usage
old_sta_config = {
    'K1': 35.0,
    'K2': 20.0,
    'gains': [25.0, 18.0, 12.0, 8.0],  # Surface gains
    'alpha_power': 0.5,
    'switching_function_type': 'tanh',
    'max_force': 150.0
}

new_sta_config = migrate_sta_smc_manually(old_sta_config)
print("Migrated STA-SMC config:", new_sta_config)