# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 8
# Runnable: False
# Hash: c43da011

@dataclass(frozen=True)
class SMCConfig:
    gains: List[float]
    max_force: float
    dt: float
    boundary_layer: float = 0.01

    def __post_init__(self):
        # Validation logic
        if self.max_force <= 0:
            raise ValueError("max_force must be positive")