# Example from: docs\technical\pso_integration_workflows.md
# Index: 3
# Runnable: True
# Hash: deb84d29

class ControllerType(Enum):
    """Controller types for PSO optimization."""
    CLASSICAL_SMC = "classical_smc"
    ADAPTIVE_SMC = "adaptive_smc"
    STA_SMC = "sta_smc"
    HYBRID_SMC = "hybrid_adaptive_sta_smc"