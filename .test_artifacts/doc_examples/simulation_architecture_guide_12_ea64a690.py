# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 12
# Runnable: False
# Hash: ea64a690

# example-metadata:
# runnable: false

class SimulationContext:
    """Simulation setup and configuration management."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config = load_config(config_path, allow_unknown=True)
        self.dynamics_model = self._initialize_dynamics_model()

    def _initialize_dynamics_model(self):
        """Select dynamics model based on config flag."""
        if self.config.simulation.use_full_dynamics:
            return FullDIPDynamics(self.config.physics)
        else:
            return DoubleInvertedPendulum(self.config.physics)

    def get_dynamics_model(self):
        """Return initialized dynamics model."""
        return self.dynamics_model

    def create_controller(self, name=None, gains=None):
        """Create controller using factory."""
        # Uses default gains from config if not provided
        return create_controller(name or "classical_smc", config=self.config, gains=gains)