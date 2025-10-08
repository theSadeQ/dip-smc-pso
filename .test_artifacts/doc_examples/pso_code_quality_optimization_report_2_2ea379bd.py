# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 2
# Runnable: True
# Hash: 2ea379bd

# Enhanced type annotations example
def optimize(self, problem: OptimizationProblem, **kwargs) -> OptimizationResult:
    """Perform PSO optimization with comprehensive type safety."""

def _fitness(self, particles: np.ndarray) -> np.ndarray:
    """Vectorised fitness function with proper array typing."""

def _combine_costs(self, costs: np.ndarray) -> np.ndarray:
    """Cost aggregation with explicit return type annotation."""