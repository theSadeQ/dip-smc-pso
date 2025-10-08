# Example from: docs\controllers\factory_system_guide.md
# Index: 30
# Runnable: False
# Hash: 3f1c70dc

# 1. Use frozen dataclasses for immutable configuration
@dataclass(frozen=True)
class ControllerConfig:
    gains: List[float]
    max_force: float

# 2. Validate parameters in __post_init__
def __post_init__(self):
    if self.max_force <= 0:
        raise ValueError("max_force must be positive")

# 3. Provide sensible defaults
boundary_layer: float = 0.01
dt: float = 0.01