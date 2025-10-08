# Example from: docs\factory_integration_documentation.md
# Index: 10
# Runnable: False
# Hash: c7336748

def check_deprecated_config(controller_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Check for deprecated parameters and apply migrations."""

    # Handle deprecated parameter names
    deprecated_mappings = {
        'use_equivalent': 'enable_equivalent_control',
        'k_gain': 'switching_gain',
        'lambda_gains': 'surface_gains'
    }

    migrated_params = params.copy()
    for old_param, new_param in deprecated_mappings.items():
        if old_param in migrated_params:
            migrated_params[new_param] = migrated_params.pop(old_param)
            logger.warning(f"Parameter '{old_param}' is deprecated. Use '{new_param}' instead.")

    return migrated_params