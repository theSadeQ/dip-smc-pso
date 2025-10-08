# Example from: docs\PATTERNS.md
# Index: 12
# Runnable: False
# Hash: 790b600b

# example-metadata:
# runnable: false

# src/controllers/factory.py (lines 569-580)

def create_controller(controller_type: str, config: Optional[Any] = None):
    # Create dynamics model from config
    dynamics_model = None
    if config is not None and hasattr(config, 'physics'):
        dynamics_model = DIPDynamics(config.physics)

    # Inject dynamics into controller
    if dynamics_model is not None:
        config_params['dynamics_model'] = dynamics_model

    return controller_class(**config_params)