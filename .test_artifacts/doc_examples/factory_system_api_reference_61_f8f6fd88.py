# Example from: docs\api\factory_system_api_reference.md
# Index: 61
# Runnable: True
# Hash: f8f6fd88

# Import new controller
from src.controllers.new_controller import NewController
from src.controllers.new_controller_config import NewControllerConfig

# Add to registry
CONTROLLER_REGISTRY['new_controller'] = {
    'class': NewController,
    'config_class': NewControllerConfig,
    'default_gains': [10.0, 8.0, 5.0, 3.0],  # Reasonable defaults
    'gain_count': 4,
    'description': 'New advanced controller',
    'supports_dynamics': True,  # Whether it uses dynamics_model
    'required_params': ['gains', 'max_force', 'dt']
}