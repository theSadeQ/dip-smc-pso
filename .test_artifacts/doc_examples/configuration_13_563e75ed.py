# Example from: docs\guides\api\configuration.md
# Index: 13
# Runnable: False
# Hash: 563e75ed

@dataclass
class PSOConfig:
    """PSO configuration with sensible defaults."""
    n_particles: int = 30
    iters: int = 100
    w: float = 0.7298        # Canonical PSO inertia
    c1: float = 1.49618      # Cognitive coefficient
    c2: float = 1.49618      # Social coefficient

    def __post_init__(self):
        """Validate PSO parameters."""
        if self.n_particles < 10:
            raise ValueError("Swarm too small (min 10 particles)")
        if self.iters < 20:
            raise ValueError("Too few iterations (min 20)")