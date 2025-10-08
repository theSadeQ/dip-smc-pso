# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 1
# Runnable: False
# Hash: 27fadf3a

class ControllerProtocol(Protocol):
    def compute_control(
        self,
        state: np.ndarray,
        state_vars: Dict[str, Any],
        history: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any], Dict[str, Any]]:
        ...

    def initialize_history(self) -> Dict[str, Any]:
        ...