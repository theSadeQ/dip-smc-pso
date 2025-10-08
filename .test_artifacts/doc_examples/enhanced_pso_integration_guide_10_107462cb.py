# Example from: docs\factory\enhanced_pso_integration_guide.md
# Index: 10
# Runnable: True
# Hash: 107462cb

class PSO_ConvergenceDetector:
    """
    Advanced convergence detection for PSO optimization.

    Features:
    - Multiple convergence criteria
    - Statistical significance testing
    - Plateau detection
    - Diversity monitoring
    """

    def __init__(self, patience: int = 20, tolerance: float = 1e-6):
        self.patience = patience
        self.tolerance = tolerance
        self.fitness_history = []
        self.diversity_history = []
        self.best_fitness = float('inf')
        self.stagnation_count = 0

    def update(self, current_fitness: float, population_diversity: float) -> bool:
        """
        Update convergence detector with current optimization state.

        Returns:
            True if convergence detected, False otherwise
        """

        self.fitness_history.append(current_fitness)
        self.diversity_history.append(population_diversity)

        # Check for improvement
        if current_fitness < self.best_fitness - self.tolerance:
            self.best_fitness = current_fitness
            self.stagnation_count = 0
        else:
            self.stagnation_count += 1

        # Multiple convergence criteria
        return (
            self._check_fitness_plateau() or
            self._check_diversity_collapse() or
            self._check_statistical_convergence()
        )

    def _check_fitness_plateau(self) -> bool:
        """Check if fitness has plateaued."""
        return self.stagnation_count >= self.patience

    def _check_diversity_collapse(self) -> bool:
        """Check if population diversity has collapsed."""
        if len(self.diversity_history) < 10:
            return False

        recent_diversity = np.mean(self.diversity_history[-10:])
        return recent_diversity < 1e-8  # Very low diversity

    def _check_statistical_convergence(self) -> bool:
        """Check statistical significance of convergence."""
        if len(self.fitness_history) < 30:
            return False

        # Test if recent improvements are statistically significant
        recent_fitness = self.fitness_history[-15:]
        older_fitness = self.fitness_history[-30:-15]

        from scipy.stats import ttest_ind
        statistic, p_value = ttest_ind(recent_fitness, older_fitness)

        # If no significant difference, consider converged
        return p_value > 0.05