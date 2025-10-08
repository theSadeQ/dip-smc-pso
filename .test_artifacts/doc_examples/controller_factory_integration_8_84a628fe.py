# Example from: docs\technical\controller_factory_integration.md
# Index: 8
# Runnable: True
# Hash: 84a628fe

def resolve_dynamics_model(config):
    """Resolve dynamics model from configuration."""
    if hasattr(config, 'dynamics_model'):
        return config.dynamics_model
    elif hasattr(config, 'physics'):
        return DoubleInvertedPendulum(config.physics)
    elif hasattr(config, 'dip_params'):
        return DoubleInvertedPendulum(config.dip_params)
    return None