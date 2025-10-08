# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 2
# Runnable: False
# Hash: b87dfbf4

class Controller(ABC):
    def compute_control(
        self,
        state: np.ndarray,  # Can accept more general types in subclasses
        ...
    ) -> ...:
        ...