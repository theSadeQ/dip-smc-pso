# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 3
# Runnable: False
# Hash: ba9f9876

class Controller(ABC):
    def compute_control(...) -> Tuple[float, Dict, Dict]:  # Subclasses can return more specific types
        ...