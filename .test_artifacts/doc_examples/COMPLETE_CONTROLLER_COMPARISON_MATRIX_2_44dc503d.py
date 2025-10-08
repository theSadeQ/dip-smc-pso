# Example from: docs\analysis\COMPLETE_CONTROLLER_COMPARISON_MATRIX.md
# Index: 2
# Runnable: False
# Hash: 44dc503d

# All controllers implement the standardized interface:
class SMCInterface(Protocol):
    def compute_control(self, state: np.ndarray,
                       state_vars: Optional[Any] = None,
                       history: Optional[Dict] = None) -> ControlOutput

    def reset(self) -> None

    def initialize_state(self) -> Any

    def initialize_history(self) -> Dict

    @property
    def gains(self) -> List[float]

    @gains.setter
    def gains(self, gains: List[float]) -> None