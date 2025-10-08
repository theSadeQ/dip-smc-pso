# Example from: docs\technical\integration_protocols.md
# Index: 2
# Runnable: False
# Hash: 918d6b97

# example-metadata:
# runnable: false

class PlantModelRegistry:
    """Registry for plant models with validation."""

    _models = {}

    @classmethod
    def register(cls, name: str, model_class: type):
        """Register a new plant model."""
        if not issubclass(model_class, PlantModelInterface):
            raise TypeError("Model must implement PlantModelInterface")

        cls._models[name] = model_class

    @classmethod
    def create_model(cls, name: str, config: dict) -> PlantModelInterface:
        """Create plant model instance."""
        if name not in cls._models:
            raise ValueError(f"Unknown plant model: {name}")

        model_class = cls._models[name]
        return model_class(config)

    @classmethod
    def list_models(cls) -> List[str]:
        """List available plant models."""
        return list(cls._models.keys())

# Register built-in models
PlantModelRegistry.register('simplified_dip', SimplifiedDIPDynamics)
PlantModelRegistry.register('full_dip', FullDIPDynamics)
PlantModelRegistry.register('low_rank_dip', LowRankDIPDynamics)