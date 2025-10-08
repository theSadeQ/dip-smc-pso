# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 14
# Runnable: True
# Hash: 979c35a7

from src.controllers.factory.core.registry import ControllerRegistry

# View registered controllers
registry = ControllerRegistry()
registered_types = registry.list_controllers()

print("Registered Controllers:")
for ctrl_type in registered_types:
    factory_fn = registry.get_factory(ctrl_type)
    print(f"  {ctrl_type.value}: {factory_fn.__name__}")

# Register custom controller (plugin architecture)
def create_custom_smc(config):
    return CustomSMC(**config)

registry.register(SMCType.CUSTOM, create_custom_smc)