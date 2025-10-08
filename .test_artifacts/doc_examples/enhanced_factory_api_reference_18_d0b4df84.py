# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 18
# Runnable: True
# Hash: d0b4df84

def create_classical_smc_controller(config=None, gains=None):
    """Legacy interface for classical SMC (backward compatibility)."""
    return create_controller('classical_smc', config, gains)

def create_controller_legacy(controller_type, config=None, gains=None):
    """Legacy factory function (backward compatibility)."""
    return create_controller(controller_type, config, gains)