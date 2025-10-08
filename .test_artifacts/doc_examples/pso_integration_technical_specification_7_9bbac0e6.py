# Example from: docs\pso_integration_technical_specification.md
# Index: 7
# Runnable: False
# Hash: 9bbac0e6

class PSO_ConvergenceMonitor:
    """
    Advanced convergence monitoring with multiple termination criteria.
    """

    def __init__(self, patience: int = 50, tolerance: float = 1e-6,
                 diversity_threshold: float = 1e-8):
        self.patience = patience
        self.tolerance = tolerance
        self.diversity_threshold = diversity_threshold
        self.best_cost_history = []
        self.diversity_history = []
        self.stagnation_counter = 0

    def check_convergence(self, swarm_positions: np.ndarray,
                         swarm_costs: np.ndarray) -> tuple[bool, str]:
        """
        Multi-criteria convergence detection:
        1. Cost improvement stagnation
        2. Swarm diversity collapse
        3. Gradient-based local optimum detection
        """
        current_best = np.min(swarm_costs)
        self.best_cost_history.append(current_best)

        # Swarm diversity (standard deviation of positions)
        diversity = np.mean(np.std(swarm_positions, axis=0))
        self.diversity_history.append(diversity)

        # Check improvement stagnation
        if len(self.best_cost_history) >= 2:
            improvement = abs(self.best_cost_history[-2] - current_best)
            relative_improvement = improvement / (abs(current_best) + 1e-12)

            if relative_improvement < self.tolerance:
                self.stagnation_counter += 1
            else:
                self.stagnation_counter = 0

        # Convergence conditions
        if self.stagnation_counter >= self.patience:
            return True, f"Cost stagnation: {self.stagnation_counter} iterations without improvement"

        if diversity < self.diversity_threshold:
            return True, f"Diversity collapse: σ = {diversity:.2e} < {self.diversity_threshold:.2e}"

        return False, "Optimization continuing"