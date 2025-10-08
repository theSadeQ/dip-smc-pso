# Example from: docs\api\optimization_module_api_reference.md
# Index: 12
# Runnable: False
# Hash: 250f77b6

# example-metadata:
# runnable: false

@dataclass
class ConvergenceMetrics:
    """Comprehensive convergence metrics."""
    iteration: int                          # Current iteration number
    best_fitness: float                     # Current best fitness value
    mean_fitness: float                     # Mean fitness across swarm
    fitness_std: float                      # Fitness standard deviation
    population_diversity: float             # Swarm diversity measure
    convergence_velocity: float             # Rate of convergence
    improvement_rate: float                 # Relative improvement rate
    stagnation_score: float                 # Stagnation indicator [0, 1]
    diversity_loss_rate: float              # Rate of diversity decrease
    predicted_iterations_remaining: int     # Estimated iterations to convergence
    confidence_level: float                 # Statistical confidence [0, 1]
    convergence_probability: float          # Probability of convergence [0, 1]