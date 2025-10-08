# Example from: docs\reference\optimization\core_interfaces.md
# Index: 1
# Runnable: False
# Hash: bfdec01d

# example-metadata:
# runnable: false

class OptimizationAlgorithm(Protocol):
    def optimize(self, problem: OptimizationProblem) -> OptimizationResult:
        ...