# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 12
# Runnable: False
# Hash: 854d3209

# example-metadata:
# runnable: false

class AdaptivePSO(PSOTuner):
    """PSO with adaptive parameters based on convergence."""

    def adapt_parameters(self, iteration, diversity, improvement):
        """Adapt PSO parameters during optimization."""

        if diversity < 0.01:  # Low diversity
            self.cognitive_weight *= 1.1  # Increase exploration
            self.social_weight *= 0.9

        if improvement < 0.001:  # Slow improvement
            self.inertia_weight *= 0.95  # Decrease inertia

        # Restart mechanism for stagnation
        if iteration > 50 and improvement < 1e-6:
            self.restart_particles(fraction=0.3)