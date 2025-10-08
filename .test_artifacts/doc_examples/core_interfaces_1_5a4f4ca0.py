# Example from: docs\reference\optimization\core_interfaces.md
# Index: 1
# Runnable: False
# Hash: 5a4f4ca0

class OptimizationAlgorithm(Protocol):
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        ...