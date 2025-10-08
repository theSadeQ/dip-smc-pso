# Example from: docs\mathematical_foundations\config_validation_specification.md
# Index: 25
# Runnable: False
# Hash: 6c2beb42

# example-metadata:
# runnable: false

def migrate_legacy_config(legacy_dict: dict) -> ClassicalSMCConfig:
    """Migrate legacy configuration format."""

    # Map old parameter names to new names
    if 'epsilon' in legacy_dict:
        legacy_dict['boundary_layer'] = legacy_dict.pop('epsilon')

    if 'control_gains' in legacy_dict:
        legacy_dict['gains'] = legacy_dict.pop('control_gains')

    # Add missing defaults
    if 'boundary_layer_slope' not in legacy_dict:
        legacy_dict['boundary_layer_slope'] = 0.0

    if 'switch_method' not in legacy_dict:
        legacy_dict['switch_method'] = "tanh"

    return ClassicalSMCConfig.from_dict(legacy_dict)