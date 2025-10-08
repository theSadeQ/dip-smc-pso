# Example from: docs\reference\simulation\integrators_factory.md
# Index: 2
# Runnable: False
# Hash: a4709739

class IntegratorFactory:
    _registry = {}

    @classmethod
    def register(cls, name, integrator_class):
        cls._registry[name] = integrator_class

    @classmethod
    def create(cls, method_name, config):
        if method_name not in cls._registry:
            raise ValueError(f"Unknown integrator: {method_name}")
        return cls._registry[method_name](config)