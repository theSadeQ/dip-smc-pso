# Example from: docs\factory\configuration_reference.md
# Index: 14
# Runnable: False
# Hash: 72d75c29

# example-metadata:
# runnable: false

def _create_dynamics_model(config: Any) -> Optional[Any]:
    """Create dynamics model from configuration with fallback handling."""

    # Priority order for dynamics model resolution
    if hasattr(config, 'dynamics_model'):
        return config.dynamics_model
    elif hasattr(config, 'physics'):
        return DIPDynamics(config.physics)
    elif hasattr(config, 'dip_params'):
        return DIPDynamics(config.dip_params)
    return None