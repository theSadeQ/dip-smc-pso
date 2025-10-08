# Example from: docs\factory\deprecation_management.md
# Index: 12
# Runnable: False
# Hash: 099a3855

# example-metadata:
# runnable: false

# Global deprecation warner instance
_deprecation_warner = ControllerDeprecationWarner()

def check_deprecated_config(controller_type: str, config_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for checking and migrating deprecated parameters.

    Usage:
        config_params = check_deprecated_config('classical_smc', raw_config)
    """
    migrated_params, warnings = _deprecation_warner.check_deprecated_parameters(
        controller_type, config_params
    )
    return migrated_params

def get_deprecation_statistics() -> Dict[str, Any]:
    """Get current deprecation usage statistics."""
    return _deprecation_warner.get_migration_statistics()

def generate_migration_report() -> Dict[str, Any]:
    """Generate comprehensive migration report for analysis."""
    return _deprecation_warner.generate_deprecation_report()