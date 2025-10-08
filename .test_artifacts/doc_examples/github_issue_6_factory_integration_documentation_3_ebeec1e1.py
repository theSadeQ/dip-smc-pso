# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 3
# Runnable: True
# Hash: ebeec1e1

@dataclass(frozen=True)
class ClassicalSMCConfig:
    gains: List[float]  # [k1, k2, λ1, λ2, K, kd]

    def __post_init__(self) -> None:
        # Mathematical constraint validation
        if any(g <= 0 for g in self.gains[:5]):
            raise ValueError("Classical SMC stability requires λᵢ > 0, K > 0")