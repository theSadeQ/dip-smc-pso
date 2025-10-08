# Example from: docs\technical\pso_integration_workflows.md
# Index: 1
# Runnable: True
# Hash: e29c176f

from src.optimization.integration.pso_factory_bridge import (
    EnhancedPSOFactory, PSOFactoryConfig, ControllerType
)

class EnhancedPSOFactory:
    """Enhanced PSO-Factory integration with advanced optimization capabilities."""

    def __init__(self, config: PSOFactoryConfig, global_config_path: str = "config.yaml")
    def create_enhanced_controller_factory(self) -> Callable
    def create_enhanced_fitness_function(self, controller_factory: Callable) -> Callable
    def optimize_controller(self) -> Dict[str, Any]
    def get_optimization_diagnostics(self) -> Dict[str, Any]