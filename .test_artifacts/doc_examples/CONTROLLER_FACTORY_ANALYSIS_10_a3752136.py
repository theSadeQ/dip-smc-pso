# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 10
# Runnable: False
# Hash: a3752136

# File: src/controllers/smc/algorithms/hybrid/config.py
@dataclass(frozen=True)
class HybridSMCConfig:
    # ... existing fields ...

    # Add for PSO compatibility
    gains: List[float] = field(default_factory=lambda: [18.0, 12.0, 10.0, 8.0])

    def __post_init__(self):
        """Validate configuration after creation."""
        # Validate gains represent surface parameters [c1, λ1, c2, λ2]
        if len(self.gains) != 4:
            raise ValueError("Hybrid controller requires exactly 4 surface gains")
        # ... existing validation ...