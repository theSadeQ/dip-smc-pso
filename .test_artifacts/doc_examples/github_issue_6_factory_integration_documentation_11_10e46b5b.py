# Example from: docs\factory\github_issue_6_factory_integration_documentation.md
# Index: 11
# Runnable: True
# Hash: 10e46b5b

class SMCType(Enum):
    """Enumeration of supported SMC controller types."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"