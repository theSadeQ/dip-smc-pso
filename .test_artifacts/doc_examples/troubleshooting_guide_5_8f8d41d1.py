# Example from: docs\factory\troubleshooting_guide.md
# Index: 5
# Runnable: False
# Hash: 8f8d41d1

# example-metadata:
# runnable: false

def diagnose_config_validation(controller_type, config_params):
    print(f"Diagnosing configuration for {controller_type}")

    required_params = {
        'classical_smc': ['gains', 'max_force', 'boundary_layer', 'dt'],
        'adaptive_smc': ['gains', 'max_force', 'dt', 'leak_rate', 'adapt_rate_limit'],
        'sta_smc': ['gains', 'max_force', 'dt', 'power_exponent'],
        'hybrid_adaptive_sta_smc': ['gains', 'hybrid_mode', 'dt', 'max_force']
    }

    if controller_type in required_params:
        required = required_params[controller_type]
        provided = list(config_params.keys())

        missing = set(required) - set(provided)
        extra = set(provided) - set(required)

        if missing:
            print(f"✗ Missing required parameters: {list(missing)}")
        if extra:
            print(f"ℹ Extra parameters (optional): {list(extra)}")

        for param in required:
            if param in config_params:
                value = config_params[param]
                print(f"✓ {param}: {value}")
            else:
                print(f"✗ {param}: MISSING")
    else:
        print(f"No validation rules for {controller_type}")

# Example usage
config = {'gains': [10, 5, 8, 3, 15, 2], 'max_force': 150.0}
diagnose_config_validation('classical_smc', config)