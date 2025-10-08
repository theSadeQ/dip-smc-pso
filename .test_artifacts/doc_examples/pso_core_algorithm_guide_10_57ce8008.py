# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 10
# Runnable: False
# Hash: 57ce8008

def adaptive_strategy(self, diversity: float) -> None:
    """Adjust parameters based on swarm diversity.

    Args:
        diversity: Current swarm diversity metric
    """
    threshold_low = 0.1
    threshold_high = 0.5

    if diversity < threshold_low:
        # Low diversity → Premature convergence risk
        # Increase exploration
        self.inertia_weight = min(0.9, self.inertia_weight * 1.1)
        self.cognitive_weight = min(2.5, self.cognitive_weight * 1.1)
        self.logger.info("Low diversity detected - increasing exploration")

    elif diversity > threshold_high:
        # High diversity → Slow convergence
        # Increase exploitation
        self.inertia_weight = max(0.4, self.inertia_weight * 0.9)
        self.social_weight = min(2.5, self.social_weight * 1.1)
        self.logger.info("High diversity detected - increasing exploitation")