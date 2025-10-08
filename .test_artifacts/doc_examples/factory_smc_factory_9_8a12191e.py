# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 9
# Runnable: False
# Hash: 8a12191e

# example-metadata:
# runnable: false

class SMCConfigBuilder:
    def __init__(self):
        self._config = {}

    def with_gains(self, gains: List[float]):
        self._config['gains'] = gains
        return self

    def with_max_force(self, max_force: float):
        self._config['max_force'] = max_force
        return self

    def build(self) -> SMCConfig:
        return SMCConfig(**self._config)