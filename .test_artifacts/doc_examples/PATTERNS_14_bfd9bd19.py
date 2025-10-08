# Example from: docs\PATTERNS.md
# Index: 14
# Runnable: False
# Hash: bfd9bd19

# example-metadata:
# runnable: false

# Optional protocols for advanced features
class DynamicsAwareController(Protocol):
    """Protocol for controllers that use plant dynamics."""
    def set_dynamics(self, dynamics: DIPDynamics) -> None: ...

class AdaptiveController(Protocol):
    """Protocol for controllers with online adaptation."""
    def get_adapted_gains(self) -> List[float]: ...
    def reset_adaptation(self) -> None: ...

class ObservableController(Protocol):
    """Protocol for controllers that provide internal state."""
    def get_internal_state(self) -> Dict[str, Any]: ...