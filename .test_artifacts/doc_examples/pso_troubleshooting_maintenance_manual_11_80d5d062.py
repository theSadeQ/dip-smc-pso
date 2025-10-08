# Example from: docs\pso_troubleshooting_maintenance_manual.md
# Index: 11
# Runnable: False
# Hash: 80d5d062

class AdaptivePSOTuner(PSOTuner):
    """PSO tuner with adaptive parameter adjustment."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stagnation_threshold = 20
        self.diversity_threshold = 0.01
        self.restart_fraction = 0.3

    def adaptive_callback(self, iteration, best_cost, best_position, **kwargs):
        """Adaptive PSO parameter adjustment callback."""

        # Get swarm statistics
        diversity = kwargs.get('diversity', 0)
        cost_history = kwargs.get('cost_history', [])

        # Detect stagnation
        if len(cost_history) > self.stagnation_threshold:
            recent_improvement = cost_history[-self.stagnation_threshold] - cost_history[-1]
            if recent_improvement < 1e-6:
                print(f"🔄 Stagnation detected at iteration {iteration} - adapting parameters")
                self._adapt_for_stagnation()

        # Detect low diversity
        if diversity < self.diversity_threshold:
            print(f"🌟 Low diversity detected at iteration {iteration} - increasing exploration")
            self._adapt_for_low_diversity()

        # Convergence acceleration
        if iteration > 100 and iteration % 50 == 0:
            self._adapt_for_convergence(iteration)

        return False  # Continue optimization

    def _adapt_for_stagnation(self):
        """Adapt parameters for stagnation recovery."""
        # Increase cognitive weight, decrease social weight
        self.cognitive_weight *= 1.2
        self.social_weight *= 0.8

        # Restart some particles
        n_restart = int(self.n_particles * self.restart_fraction)
        # ... particle restart implementation

    def _adapt_for_low_diversity(self):
        """Adapt parameters for diversity enhancement."""
        # Increase inertia weight temporarily
        self.inertia_weight = min(0.9, self.inertia_weight * 1.1)

        # Increase velocity limits
        if hasattr(self, 'velocity_clamp'):
            self.velocity_clamp = [v * 1.2 for v in self.velocity_clamp]

    def _adapt_for_convergence(self, iteration):
        """Adapt parameters for convergence acceleration."""
        progress = iteration / self.max_iterations

        # Linear adaptation schedule
        self.inertia_weight = 0.9 - 0.5 * progress
        self.cognitive_weight = 2.0 - 0.5 * progress
        self.social_weight = 0.5 + 1.5 * progress