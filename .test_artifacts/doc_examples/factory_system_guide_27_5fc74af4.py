# Example from: docs\controllers\factory_system_guide.md
# Index: 27
# Runnable: False
# Hash: 5fc74af4

# example-metadata:
# runnable: false

def _create_dynamics_model(config: Any) -> Optional[Any]:
    """Create dynamics model from configuration."""

    # Try to get existing dynamics model
    if hasattr(config, 'dynamics_model'):
        return config.dynamics_model
    elif hasattr(config, 'physics'):
        return DIPDynamics(config.physics)
    elif hasattr(config, 'dip_params'):
        return DIPDynamics(config.dip_params)

    return None