# Example from: docs\reports\DOCUMENTATION_EXPERT_TECHNICAL_ASSESSMENT_REPORT.md
# Index: 4
# Runnable: False
# Hash: d6343893

# example-metadata:
# runnable: false

@dataclass
class MonteCarloConfig:
    """Configuration for Monte Carlo analysis."""
    # Basic simulation parameters
    n_samples: int = 1000
    confidence_level: float = 0.95

    # Sampling methods
    sampling_method: str = "random"  # "random", "latin_hypercube", "sobol", "halton"
    antithetic_variates: bool = False
    control_variates: bool = False