# Example from: docs\controllers\factory_system_guide.md
# Index: 12
# Runnable: False
# Hash: 48dfa4a0

@dataclass(frozen=True)
class SMCGainSpec:
    """Specification of gain requirements for each SMC type."""
    controller_type: SMCType
    n_gains: int
    gain_names: List[str]
    description: str

    @property
    def gain_bounds(self) -> List[tuple[float, float]]:
        """Default gain bounds for PSO optimization."""
        if self.controller_type == SMCType.CLASSICAL:
            # [k1, k2, lam1, lam2, K, kd]
            return [(0.1, 50.0)] * 4 + [(1.0, 200.0)] + [(0.0, 50.0)]
        # ... controller-specific bounds

# Pre-defined specifications
SMC_GAIN_SPECS = {
    SMCType.CLASSICAL: SMCGainSpec(
        SMCType.CLASSICAL, 6,
        ["k1", "k2", "lam1", "lam2", "K", "kd"],
        "Classical SMC with switching and damping gains"
    ),
    # ... additional specifications
}