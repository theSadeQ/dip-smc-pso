# Example from: docs\factory\migration_guide.md
# Index: 8
# Runnable: False
# Hash: af9739a5

# example-metadata:
# runnable: false

def migrate_hybrid_smc_manually(old_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Manual migration procedure for Hybrid SMC configurations.

    Changes:
    1. Rename 'mode' to 'hybrid_mode'
    2. Replace 'sub_controller_gains' with full sub-configurations
    3. Update 'switch_threshold' to 'switching_criteria'
    """

    new_config = {}

    # Step 1: Handle surface gains (4 elements for hybrid controller)
    gains = old_config.get('gains', [18.0, 12.0, 10.0, 8.0])
    new_config['gains'] = gains[:4]  # Ensure exactly 4 surface gains

    # Step 2: Handle mode parameter
    if 'mode' in old_config:
        new_config['hybrid_mode'] = old_config['mode']
        print(f"Migrated: mode -> hybrid_mode")
    else:
        new_config['hybrid_mode'] = 'CLASSICAL_ADAPTIVE'  # Default

    # Step 3: Handle sub-controller configurations
    if 'sub_controller_gains' in old_config:
        sub_gains = old_config['sub_controller_gains']

        # Create proper sub-configurations
        if isinstance(sub_gains, dict):
            classical_gains = sub_gains.get('classical', [20.0, 15.0, 12.0, 8.0, 35.0, 5.0])
            adaptive_gains = sub_gains.get('adaptive', [25.0, 18.0, 15.0, 10.0, 4.0])
        else:
            # Use defaults if format is unrecognized
            classical_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
            adaptive_gains = [25.0, 18.0, 15.0, 10.0, 4.0]

        # Create full sub-configurations
        new_config['classical_config'] = {
            'gains': classical_gains,
            'max_force': 150.0,
            'dt': 0.001,
            'boundary_layer': 0.02
        }

        new_config['adaptive_config'] = {
            'gains': adaptive_gains,
            'max_force': 150.0,
            'dt': 0.001,
            'leak_rate': 0.01,
            'adapt_rate_limit': 10.0,
            'K_min': 0.1,
            'K_max': 100.0,
            'K_init': 10.0,
            'alpha': 0.5
        }

        print("Converted: sub_controller_gains -> full sub-configurations")

    # Step 4: Handle switching criteria
    if 'switch_threshold' in old_config:
        threshold = old_config['switch_threshold']
        new_config['switching_criteria'] = {
            'error_threshold': threshold,
            'time_threshold': 2.0  # Default
        }
        print("Converted: switch_threshold -> switching_criteria")

    # Step 5: Copy valid parameters
    valid_params = [
        'dt', 'max_force', 'k1_init', 'k2_init', 'gamma1', 'gamma2',
        'dynamics_model', 'hybrid_mode', 'classical_config', 'adaptive_config'
    ]

    for param in valid_params:
        if param in old_config:
            new_config[param] = old_config[param]

    # Step 6: Ensure required parameters have defaults
    new_config.setdefault('dt', 0.001)
    new_config.setdefault('max_force', 150.0)
    new_config.setdefault('k1_init', 5.0)
    new_config.setdefault('k2_init', 3.0)
    new_config.setdefault('gamma1', 0.5)
    new_config.setdefault('gamma2', 0.3)

    return new_config

# Example usage
old_hybrid_config = {
    'gains': [18.0, 12.0, 10.0, 8.0],
    'mode': 'CLASSICAL_ADAPTIVE',
    'sub_controller_gains': {
        'classical': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'adaptive': [25.0, 18.0, 15.0, 10.0, 4.0]
    },
    'switch_threshold': 0.1,
    'max_force': 150.0
}

new_hybrid_config = migrate_hybrid_smc_manually(old_hybrid_config)
print("Migrated Hybrid SMC config:", new_hybrid_config)