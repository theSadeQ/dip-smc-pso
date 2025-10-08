# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 27
# Runnable: False
# Hash: 423e594b

def create_controllers_from_config(config_dict):
    controllers = {}
    for controller_type, params in config_dict['controllers'].items():
        controllers[controller_type] = create_controller(
            controller_type,
            gains=params['gains'],
            max_force=params.get('max_force', 100.0),
            boundary_layer=params.get('boundary_layer', 0.01)
        )
    return controllers