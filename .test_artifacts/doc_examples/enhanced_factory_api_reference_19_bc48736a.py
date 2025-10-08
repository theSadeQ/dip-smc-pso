# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 19
# Runnable: True
# Hash: bc48736a

def check_deprecated_config(controller_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check for deprecated parameters and apply migrations.

    Returns:
        Updated parameter dictionary with migrations applied
    """