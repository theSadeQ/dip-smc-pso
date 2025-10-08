# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 16
# Runnable: True
# Hash: bbb16674

def validate_yaml_configuration(config_path):
    """Validate YAML configuration file."""

    import yaml
    from pathlib import Path

    print(f"Validating configuration: {config_path}")

    # Check file exists
    if not Path(config_path).exists():
        print(f"❌ Configuration file not found: {config_path}")
        return False

    # Check YAML syntax
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        print("✅ YAML syntax valid")
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False

    # Check required sections
    required_sections = ['controllers', 'physics', 'simulation']
    for section in required_sections:
        if section not in config_data:
            print(f"⚠️  Missing section: {section}")
        else:
            print(f"✅ Section found: {section}")

    # Check controller configurations
    if 'controllers' in config_data:
        controllers = config_data['controllers']

        for controller_type, controller_config in controllers.items():
            print(f"\nValidating {controller_type}:")

            # Check gains
            if 'gains' in controller_config:
                gains = controller_config['gains']
                if not isinstance(gains, list):
                    print(f"  ❌ gains must be a list, got {type(gains)}")
                elif len(gains) == 0:
                    print(f"  ❌ gains list is empty")
                else:
                    print(f"  ✅ gains: {len(gains)} values")

            # Check numeric parameters
            numeric_params = ['max_force', 'dt', 'boundary_layer']
            for param in numeric_params:
                if param in controller_config:
                    value = controller_config[param]
                    if not isinstance(value, (int, float)):
                        print(f"  ❌ {param} must be numeric, got {type(value)}")
                    elif value <= 0:
                        print(f"  ❌ {param} must be positive, got {value}")
                    else:
                        print(f"  ✅ {param}: {value}")

    return True

# Validate configuration
validate_yaml_configuration("config.yaml")