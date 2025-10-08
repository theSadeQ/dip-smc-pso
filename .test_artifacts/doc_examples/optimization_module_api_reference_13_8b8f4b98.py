# Example from: docs\api\optimization_module_api_reference.md
# Index: 13
# Runnable: False
# Hash: 8b8f4b98

# example-metadata:
# runnable: false

@dataclass
class ConvergenceCriteria:
    """Adaptive convergence criteria configuration."""

    # Fitness-based criteria
    fitness_tolerance: float = 1e-6
    relative_improvement_threshold: float = 1e-4

    # Diversity-based criteria
    min_diversity_threshold: float = 1e-3
    diversity_loss_rate_threshold: float = 0.95

    # Stagnation detection
    stagnation_window: int = 10
    stagnation_threshold: float = 1e-5

    # Statistical criteria
    statistical_confidence_level: float = 0.95
    min_sample_size: int = 20

    # Adaptive parameters
    enable_adaptive_criteria: bool = True
    controller_specific_adjustment: bool = True

    # Performance prediction
    enable_performance_prediction: bool = True
    prediction_window: int = 15

    # Early stopping
    max_stagnation_iterations: int = 50
    premature_convergence_detection: bool = True