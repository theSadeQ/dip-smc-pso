# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 17
# Runnable: True
# Hash: feb153e5

def fix_configuration_file(config_path, backup=True):
    """Fix common configuration file issues."""

    import yaml
    import shutil
    from pathlib import Path

    config_file = Path(config_path)

    if backup:
        backup_file = config_file.with_suffix('.yaml.backup')
        shutil.copy2(config_file, backup_file)
        print(f"Created backup: {backup_file}")

    # Load current configuration
    with open(config_file, 'r') as f:
        config_data = yaml.safe_load(f)

    fixes_applied = []

    # Fix 1: Ensure required sections exist
    required_sections = {
        'controllers': {},
        'physics': {
            'm1': 0.5, 'm2': 0.5, 'M': 2.0,
            'l1': 0.5, 'l2': 0.5,
            'b1': 0.1, 'b2': 0.1, 'I1': 0.1, 'I2': 0.1
        },
        'simulation': {
            'duration': 5.0,
            'dt': 0.001
        }
    }

    for section, defaults in required_sections.items():
        if section not in config_data:
            config_data[section] = defaults
            fixes_applied.append(f"Added missing section: {section}")

    # Fix 2: Ensure controller defaults
    controller_defaults = {
        'classical_smc': {
            'gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
            'max_force': 150.0,
            'boundary_layer': 0.02,
            'dt': 0.001
        },
        'adaptive_smc': {
            'gains': [25.0, 18.0, 15.0, 10.0, 4.0],
            'max_force': 150.0,
            'dt': 0.001
        },
        'sta_smc': {
            'gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],
            'max_force': 150.0,
            'dt': 0.001
        }
    }

    for controller_type, defaults in controller_defaults.items():
        if controller_type not in config_data['controllers']:
            config_data['controllers'][controller_type] = defaults
            fixes_applied.append(f"Added controller defaults: {controller_type}")
        else:
            # Fix missing parameters
            controller_config = config_data['controllers'][controller_type]
            for param, default_value in defaults.items():
                if param not in controller_config:
                    controller_config[param] = default_value
                    fixes_applied.append(f"Added missing parameter {controller_type}.{param}")

    # Fix 3: Validate and fix data types
    for controller_type, controller_config in config_data['controllers'].items():
        if 'gains' in controller_config:
            gains = controller_config['gains']
            if not isinstance(gains, list):
                # Try to convert to list
                try:
                    controller_config['gains'] = list(gains)
                    fixes_applied.append(f"Converted {controller_type}.gains to list")
                except:
                    controller_config['gains'] = controller_defaults.get(controller_type, {}).get('gains', [1.0])
                    fixes_applied.append(f"Reset invalid {controller_type}.gains")

    # Write fixed configuration
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

    if fixes_applied:
        print("Fixes applied:")
        for fix in fixes_applied:
            print(f"  ✅ {fix}")
    else:
        print("No fixes needed")

    return len(fixes_applied) > 0

# Fix configuration file
fix_configuration_file("config.yaml")