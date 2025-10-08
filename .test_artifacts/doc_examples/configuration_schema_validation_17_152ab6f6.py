# Example from: docs\configuration_schema_validation.md
# Index: 17
# Runnable: False
# Hash: 152ab6f6

# example-metadata:
# runnable: false

def validate_backward_compatibility(old_config: dict, new_config: dict) -> bool:
    """Validate backward compatibility between configuration versions."""

    # Core functionality must remain available
    core_sections = ['physics', 'controllers', 'simulation']
    for section in core_sections:
        if section in old_config and section not in new_config:
            raise ValueError(f"Core section {section} removed in new configuration")

    # Controller types must remain supported
    old_controllers = set(old_config.get('controllers', {}).keys())
    new_controllers = set(new_config.get('controllers', {}).keys())

    removed_controllers = old_controllers - new_controllers
    if removed_controllers:
        raise ValueError(f"Controller types removed: {removed_controllers}")

    return True