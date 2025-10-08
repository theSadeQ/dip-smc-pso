# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 3
# Runnable: False
# Hash: a8befa21

# example-metadata:
# runnable: false

@dataclass(frozen=True)
class HybridSMCConfig:
    # ... existing fields ...

    # Add gains property for PSO compatibility
    gains: List[float] = field(default_factory=lambda: [18.0, 12.0, 10.0, 8.0])

    @property
    def surface_gains(self) -> List[float]:
        """Surface parameters for sliding mode design [c1, λ1, c2, λ2]"""
        return self.gains