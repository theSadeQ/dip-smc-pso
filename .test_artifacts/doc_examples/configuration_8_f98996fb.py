# Example from: docs\guides\api\configuration.md
# Index: 8
# Runnable: False
# Hash: f98996fb

@dataclass
class SimulationConfig:
    """Simulation parameters."""
    duration: float = Field(..., gt=0)
    dt: float = Field(..., gt=0, le=0.1)
    use_full_dynamics: bool = False