# Example from: docs\factory\factory_integration_user_guide.md
# Index: 18
# Runnable: False
# Hash: 9a318b74

# example-metadata:
# runnable: false

class LazyControllerEnsemble:
    """Lazy-loaded controller ensemble for memory efficiency."""

    def __init__(self, controller_specs, config):
        self.specs = controller_specs
        self.config = config
        self._controllers = {}

    def get_controller(self, controller_type):
        if controller_type not in self._controllers:
            spec = self.specs[controller_type]
            self._controllers[controller_type] = create_controller(
                controller_type, config=self.config, **spec
            )
        return self._controllers[controller_type]