# Example from: docs\architecture\controller_system_architecture.md
# Index: 8
# Runnable: False
# Hash: 59cf96b9

# example-metadata:
# runnable: false

class ControllerInterface(Protocol):
    """Standardized interface for all SMC controllers."""

    def compute_control(
        self,
        state: np.ndarray,
        state_vars: Optional[Tuple[float, ...]] = None,
        history: Optional[Dict[str, List[Any]]] = None
    ) -> ControllerOutput:
        """
        Compute control action for given state.

        Args:
            state: System state [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]
            state_vars: Controller internal state variables
            history: Control history for logging and analysis

        Returns:
            ControllerOutput: Named tuple with control, state_vars, history
        """
        ...

    def reset(self) -> None:
        """Reset controller to initial state."""
        ...

    def initialize_state(self) -> Tuple[float, ...]:
        """Initialize controller state variables."""
        ...