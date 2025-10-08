# Example from: docs\api\optimization_module_api_reference.md
# Index: 25
# Runnable: True
# Hash: f31b7fe2

class OptimizationObjective(Enum):
    """Meta-optimization objectives."""
    CONVERGENCE_SPEED = "convergence_speed"     # Minimize iterations to convergence
    SOLUTION_QUALITY = "solution_quality"       # Minimize final cost
    ROBUSTNESS = "robustness"                   # Minimize performance variance
    EFFICIENCY = "efficiency"                   # Balance quality vs. computational cost
    MULTI_OBJECTIVE = "multi_objective"         # Weighted combination