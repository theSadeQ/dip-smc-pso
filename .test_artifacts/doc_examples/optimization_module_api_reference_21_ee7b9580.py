# Example from: docs\api\optimization_module_api_reference.md
# Index: 21
# Runnable: True
# Hash: ee7b9580

class BoundsOptimizationStrategy(Enum):
    """Bounds optimization strategies."""
    PHYSICS_BASED = "physics_based"              # Stability-constrained bounds
    PERFORMANCE_DRIVEN = "performance_driven"    # Empirically validated bounds
    CONVERGENCE_FOCUSED = "convergence_focused"  # PSO-optimized bounds
    HYBRID = "hybrid"                            # Weighted combination