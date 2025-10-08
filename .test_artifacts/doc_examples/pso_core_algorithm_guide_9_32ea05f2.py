# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 9
# Runnable: False
# Hash: 32ea05f2

# example-metadata:
# runnable: false

def update_adaptive_parameters(self, iteration: int) -> None:
    """Update PSO parameters based on iteration progress.

    Args:
        iteration: Current iteration number
    """
    if not self.adaptive_weights:
        return

    # Progress ratio [0, 1]
    progress = iteration / self.max_iterations

    # Linear decreasing inertia weight
    self.inertia_weight = (
        self.initial_inertia -
        (self.initial_inertia - self.final_inertia) * progress
    )

    # Time-varying cognitive coefficient
    self.cognitive_weight = (
        self.initial_c1 -
        (self.initial_c1 - self.final_c1) * progress
    )

    # Time-varying social coefficient
    self.social_weight = (
        self.initial_c2 +
        (self.final_c2 - self.initial_c2) * progress
    )

    self.logger.debug(
        f"Iteration {iteration}: ω={self.inertia_weight:.3f}, "
        f"c1={self.cognitive_weight:.3f}, c2={self.social_weight:.3f}"
    )