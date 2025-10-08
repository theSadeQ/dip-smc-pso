# Example from: docs\api\factory_system_api_reference.md
# Index: 58
# Runnable: True
# Hash: 032fc69d

from src.controllers.factory import create_controller
from src.config import load_config

def validate_configuration_before_creation(config_path):
    """Validate configuration file before controller creation."""
    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"Failed to load config: {e}")
        return False

    # Check required sections exist
    if not hasattr(config, 'controllers'):
        print("Config missing 'controllers' section")
        return False

    # Validate each controller configuration
    for controller_type in ['classical_smc', 'sta_smc', 'adaptive_smc']:
        try:
            controller = create_controller(controller_type, config)
            print(f"✓ {controller_type} config valid")
        except Exception as e:
            print(f"✗ {controller_type} config invalid: {e}")
            return False

    return True