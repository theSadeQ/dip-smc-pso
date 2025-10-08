# Example from: docs\factory\migration_guide.md
# Index: 5
# Runnable: False
# Hash: a6642305

def migrate_classical_smc_manually(old_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Manual migration procedure for Classical SMC configurations.

    Changes:
    1. Combine gains and K_switching into 6-element gains array
    2. Remove invalid 'gamma' parameter
    3. Rename 'switch_function' to 'switch_method'
    4. Ensure boundary_layer parameter is present
    """

    new_config = {}

    # Step 1: Handle gains array
    gains = old_config.get('gains', [8.0, 6.0, 4.0, 3.0, 15.0])

    # If gains has only 5 elements, add K_switching as 6th element
    if len(gains) == 5:
        K_switching = old_config.get('K_switching', 2.0)
        gains = gains + [K_switching]
    elif len(gains) < 5:
        # Fill missing gains with defaults
        default_gains = [8.0, 6.0, 4.0, 3.0, 15.0, 2.0]
        gains = gains + default_gains[len(gains):]

    new_config['gains'] = gains[:6]  # Ensure exactly 6 gains

    # Step 2: Handle deprecated parameters
    deprecated_params = ['gamma', 'adaptation_rate', 'K_switching']
    for param in deprecated_params:
        if param in old_config:
            if param == 'gamma':
                print(f"Warning: Removed invalid 'gamma' parameter for Classical SMC")
            elif param == 'adaptation_rate':
                print(f"Warning: Removed 'adaptation_rate' - not valid for Classical SMC")
            # K_switching already handled in gains array

    # Step 3: Handle renamed parameters
    if 'switch_function' in old_config:
        new_config['switch_method'] = old_config['switch_function']
        print(f"Migrated: switch_function -> switch_method")

    # Step 4: Copy valid parameters
    valid_params = [
        'max_force', 'dt', 'boundary_layer', 'switch_method',
        'damping_gain', 'dynamics_model'
    ]

    for param in valid_params:
        if param in old_config:
            new_config[param] = old_config[param]

    # Step 5: Ensure required parameters have defaults
    new_config.setdefault('max_force', 150.0)
    new_config.setdefault('dt', 0.001)
    new_config.setdefault('boundary_layer', 0.02)

    return new_config

# Example usage
old_classical_config = {
    'gains': [10, 5, 8, 3, 15],
    'K_switching': 2.0,
    'gamma': 0.1,              # Invalid - will be removed
    'switch_function': 'sign',  # Will be renamed
    'max_force': 100.0
}

new_classical_config = migrate_classical_smc_manually(old_classical_config)
print("Migrated Classical SMC config:", new_classical_config)