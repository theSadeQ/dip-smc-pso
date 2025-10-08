# Example from: docs\factory\pso_integration_workflow.md
# Index: 6
# Runnable: False
# Hash: e0d3e381

class PSOProgressMonitor:
    """
    Comprehensive PSO optimization progress monitoring.

    Features:
    - Convergence detection
    - Performance tracking
    - Early termination criteria
    - Optimization health assessment
    """

    def __init__(
        self,
        convergence_threshold: float = 1e-6,
        stagnation_threshold: int = 20,
        max_evaluation_time: float = 0.1
    ):
        self.convergence_threshold = convergence_threshold
        self.stagnation_threshold = stagnation_threshold
        self.max_evaluation_time = max_evaluation_time

        # Progress tracking
        self.iteration_history = []
        self.best_fitness_history = []
        self.diversity_history = []
        self.evaluation_time_history = []

        # Convergence state
        self.converged = False
        self.stagnation_count = 0
        self.best_fitness = float('inf')

    def update_progress(
        self,
        iteration: int,
        swarm_positions: np.ndarray,
        fitness_values: List[float],
        evaluation_time: float
    ) -> Dict[str, Any]:
        """
        Update optimization progress and assess termination criteria.

        Returns:
            Progress update with termination recommendations
        """

        # Update best fitness
        current_best = min(fitness_values)
        improvement = self.best_fitness - current_best

        if improvement > self.convergence_threshold:
            self.best_fitness = current_best
            self.stagnation_count = 0
        else:
            self.stagnation_count += 1

        # Calculate swarm diversity
        diversity = self._calculate_swarm_diversity(swarm_positions)

        # Record history
        self.iteration_history.append(iteration)
        self.best_fitness_history.append(current_best)
        self.diversity_history.append(diversity)
        self.evaluation_time_history.append(evaluation_time)

        # Assess convergence
        convergence_status = self._assess_convergence(diversity, improvement)

        # Performance assessment
        performance_status = self._assess_performance(evaluation_time)

        # Termination recommendation
        should_terminate, termination_reason = self._should_terminate(
            convergence_status, performance_status
        )

        return {
            'iteration': iteration,
            'best_fitness': current_best,
            'improvement': improvement,
            'diversity': diversity,
            'stagnation_count': self.stagnation_count,
            'convergence_status': convergence_status,
            'performance_status': performance_status,
            'should_terminate': should_terminate,
            'termination_reason': termination_reason,
            'evaluation_time': evaluation_time
        }

    def _calculate_swarm_diversity(self, swarm_positions: np.ndarray) -> float:
        """Calculate swarm diversity metric."""
        if len(swarm_positions) < 2:
            return 0.0

        # Calculate pairwise distances
        distances = []
        for i in range(len(swarm_positions)):
            for j in range(i + 1, len(swarm_positions)):
                distance = np.linalg.norm(swarm_positions[i] - swarm_positions[j])
                distances.append(distance)

        return np.mean(distances) if distances else 0.0

    def _assess_convergence(self, diversity: float, improvement: float) -> str:
        """Assess convergence status."""
        if improvement < self.convergence_threshold and diversity < 0.01:
            return 'CONVERGED'
        elif self.stagnation_count >= self.stagnation_threshold:
            return 'STAGNATED'
        elif diversity < 0.1:
            return 'LOW_DIVERSITY'
        elif improvement > 1.0:
            return 'IMPROVING'
        else:
            return 'SEARCHING'

    def _assess_performance(self, evaluation_time: float) -> str:
        """Assess computational performance."""
        if evaluation_time > self.max_evaluation_time:
            return 'SLOW'
        elif evaluation_time > self.max_evaluation_time * 0.5:
            return 'MODERATE'
        else:
            return 'FAST'

    def _should_terminate(
        self,
        convergence_status: str,
        performance_status: str
    ) -> Tuple[bool, str]:
        """Determine if optimization should terminate early."""

        if convergence_status == 'CONVERGED':
            return True, 'Convergence achieved'

        if convergence_status == 'STAGNATED':
            return True, f'Stagnation detected ({self.stagnation_count} iterations)'

        if performance_status == 'SLOW' and len(self.evaluation_time_history) > 10:
            avg_time = np.mean(self.evaluation_time_history[-10:])
            if avg_time > self.max_evaluation_time * 2:
                return True, 'Performance degradation detected'

        return False, 'Continue optimization'

    def generate_optimization_report(self) -> Dict[str, Any]:
        """Generate comprehensive optimization report."""
        return {
            'optimization_summary': {
                'total_iterations': len(self.iteration_history),
                'best_fitness_achieved': min(self.best_fitness_history) if self.best_fitness_history else float('inf'),
                'final_diversity': self.diversity_history[-1] if self.diversity_history else 0.0,
                'convergence_status': 'CONVERGED' if self.converged else 'INCOMPLETE'
            },
            'performance_metrics': {
                'avg_evaluation_time': np.mean(self.evaluation_time_history) if self.evaluation_time_history else 0.0,
                'max_evaluation_time': np.max(self.evaluation_time_history) if self.evaluation_time_history else 0.0,
                'total_optimization_time': sum(self.evaluation_time_history)
            },
            'convergence_analysis': {
                'fitness_improvement_rate': self._calculate_improvement_rate(),
                'diversity_trend': self._calculate_diversity_trend(),
                'stagnation_periods': self._identify_stagnation_periods()
            }
        }

    def _calculate_improvement_rate(self) -> float:
        """Calculate average fitness improvement rate."""
        if len(self.best_fitness_history) < 2:
            return 0.0

        improvements = []
        for i in range(1, len(self.best_fitness_history)):
            improvement = self.best_fitness_history[i-1] - self.best_fitness_history[i]
            improvements.append(max(0, improvement))

        return np.mean(improvements)

    def _calculate_diversity_trend(self) -> str:
        """Calculate diversity trend over time."""
        if len(self.diversity_history) < 10:
            return 'INSUFFICIENT_DATA'

        recent_diversity = np.mean(self.diversity_history[-5:])
        earlier_diversity = np.mean(self.diversity_history[-10:-5])

        if recent_diversity < earlier_diversity * 0.8:
            return 'DECREASING'
        elif recent_diversity > earlier_diversity * 1.2:
            return 'INCREASING'
        else:
            return 'STABLE'

    def _identify_stagnation_periods(self) -> List[Tuple[int, int]]:
        """Identify periods of stagnation in optimization."""
        stagnation_periods = []
        current_start = None
        stagnation_threshold = 5

        for i in range(1, len(self.best_fitness_history)):
            improvement = self.best_fitness_history[i-1] - self.best_fitness_history[i]

            if improvement < self.convergence_threshold:
                if current_start is None:
                    current_start = i - 1
            else:
                if current_start is not None and i - current_start >= stagnation_threshold:
                    stagnation_periods.append((current_start, i - 1))
                current_start = None

        # Handle final stagnation period
        if current_start is not None and len(self.best_fitness_history) - current_start >= stagnation_threshold:
            stagnation_periods.append((current_start, len(self.best_fitness_history) - 1))

        return stagnation_periods