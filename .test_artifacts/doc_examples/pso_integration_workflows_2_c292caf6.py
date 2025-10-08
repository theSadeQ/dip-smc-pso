# Example from: docs\technical\pso_integration_workflows.md
# Index: 2
# Runnable: False
# Hash: c292caf6

# example-metadata:
# runnable: false

@dataclass
class PSOFactoryConfig:
    """Configuration for PSO-Factory integration."""
    controller_type: ControllerType                    # Controller to optimize
    population_size: int = 20                         # PSO swarm size
    max_iterations: int = 50                          # Maximum iterations
    convergence_threshold: float = 1e-6               # Convergence criteria
    max_stagnation_iterations: int = 10               # Early stopping
    enable_adaptive_bounds: bool = True               # Dynamic bounds
    enable_gradient_guidance: bool = False            # Gradient hints
    fitness_timeout: float = 10.0                     # Evaluation timeout [s]
    use_robust_evaluation: bool = True                # Error recovery