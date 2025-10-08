# Example from: docs\architecture\controller_system_architecture.md
# Index: 1
# Runnable: False
# Hash: a1995ee8

# Factory Registry Architecture
class ControllerRegistry:
    """Central registry for all SMC controller types."""

    _controllers: Dict[str, Type[ControllerInterface]] = {
        'classical_smc': ClassicalSMC,
        'adaptive_smc': AdaptiveSMC,
        'sta_smc': STASMC,
        'hybrid_adaptive_sta_smc': HybridAdaptiveSTASMC
    }

    @classmethod
    def register_controller(cls, name: str, controller_class: Type[ControllerInterface]):
        """Register new controller type with validation."""
        if not issubclass(controller_class, ControllerInterface):
            raise ValueError(f"Controller {name} must implement ControllerInterface")
        cls._controllers[name] = controller_class

    @classmethod
    def get_controller_class(cls, name: str) -> Type[ControllerInterface]:
        """Retrieve controller class with validation."""
        if name not in cls._controllers:
            raise ValueError(f"Unknown controller type: {name}")
        return cls._controllers[name]