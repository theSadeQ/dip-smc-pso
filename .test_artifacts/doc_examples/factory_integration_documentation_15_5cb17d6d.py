# Example from: docs\factory_integration_documentation.md
# Index: 15
# Runnable: True
# Hash: 5cb17d6d

class SMCConfig:
    """Configuration class for SMC controllers."""
    def __init__(self, gains: List[float], max_force: float = 150.0,
                 dt: float = 0.001, **kwargs: Any) -> None:
        # Configuration initialization