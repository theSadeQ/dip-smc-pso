# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 24
# Runnable: False
# Hash: be9faa98

def check_controller_api_version(controller_class: Type) -> str:
    """Check controller API version compatibility."""

    # Check for PSO interface compliance
    required_methods = ['compute_control']
    required_properties = ['max_force']
    optional_methods = ['validate_gains']

    has_required = all(hasattr(controller_class, method) for method in required_methods)
    has_properties = all(hasattr(controller_class, prop) for prop in required_properties)
    has_optional = any(hasattr(controller_class, method) for method in optional_methods)

    if has_required and has_properties:
        if has_optional:
            return "PSO_v2.0"  # Full PSO interface
        else:
            return "PSO_v1.0"  # Basic PSO interface
    else:
        return "Legacy"     # Requires adapter