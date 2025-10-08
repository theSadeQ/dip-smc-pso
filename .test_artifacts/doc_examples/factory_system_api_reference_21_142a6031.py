# Example from: docs\api\factory_system_api_reference.md
# Index: 21
# Runnable: False
# Hash: 142a6031

CONTROLLER_REGISTRY: Dict[str, Dict[str, Any]] = {
    'controller_type': {
        'class': ControllerClass,              # Controller class reference
        'config_class': ConfigClass,           # Configuration class reference
        'default_gains': List[float],          # Default gain vector
        'gain_count': int,                     # Expected number of gains
        'description': str,                    # Human-readable description
        'supports_dynamics': bool,             # Whether controller uses dynamics model
        'required_params': List[str]           # Required configuration parameters
    }
}