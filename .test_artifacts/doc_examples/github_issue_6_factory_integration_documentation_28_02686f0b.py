# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 28
# Runnable: True
# Hash: 02686f0b

def create_controllers_from_config(config_dict):
    controllers = {}
    for controller_type, params in config_dict['controllers'].items():
        smc_type = SMCType(controller_type)
        config = SMCConfig(**params)  # Type-safe parameter validation
        controllers[controller_type] = SMCFactory.create_controller(smc_type, config)
    return controllers