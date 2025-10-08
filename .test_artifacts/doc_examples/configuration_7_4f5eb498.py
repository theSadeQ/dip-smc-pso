# Example from: docs\guides\api\configuration.md
# Index: 7
# Runnable: False
# Hash: 4f5eb498

@dataclass
class ClassicalSMCConfig:
    """Classical SMC configuration."""
    gains: List[float] = Field(..., min_items=6, max_items=6)
    max_force: float = Field(..., gt=0)
    boundary_layer: float = Field(default=0.01, gt=0)

@dataclass
class AdaptiveSMCConfig:
    """Adaptive SMC configuration."""
    gains: List[float] = Field(..., min_items=5, max_items=5)
    max_force: float = Field(..., gt=0)
    adaptation_rate: float = Field(..., gt=0)
    leak_rate: float = Field(default=0.1, ge=0)
    rate_limit: float = Field(default=10.0, gt=0)