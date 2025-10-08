# Example from: docs\optimization_simulation\guide.md
# Index: 31
# Runnable: False
# Hash: 36c62727

class SimulationContext:
    """Enhanced simulation context with framework integration."""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize simulation context."""

    def get_dynamics_model(self) -> Any:
        """Return initialized dynamics model."""

    def get_config(self) -> ConfigSchema:
        """Return validated configuration."""

    def create_controller(
        self,
        name: Optional[str] = None,
        gains: Optional[List[float]] = None
    ) -> Any:
        """Create controller using configuration."""

    def create_simulation_engine(
        self,
        engine_type: str = "sequential"
    ) -> SimulationEngine:
        """
        Create simulation engine.

        Parameters
        ----------
        engine_type : str
            Engine type: 'sequential', 'batch', 'parallel', 'real_time'
        """

    def register_component(self, name: str, component: Any) -> None:
        """Register framework component."""

    def get_component(self, name: str) -> Optional[Any]:
        """Get registered component."""