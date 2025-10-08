# Example from: docs\factory\factory_api_reference.md
# Index: 25
# Runnable: True
# Hash: 841f336f

@dataclass
class SMCConfig:
    gains: List[float]
    max_force: float = 150.0
    dt: float = 0.001
    **kwargs: Any